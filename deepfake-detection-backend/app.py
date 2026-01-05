import os
import uuid
import hashlib
import json
import traceback
import cv2
import numpy as np
import base64
# import truststore
import tensorflow as tf

# ====== SOLUSI A: paksa TensorFlow pakai CPU (matikan GPU Metal) ======
try:
    tf.config.set_visible_devices([], "GPU")
    print("✅ GPU disabled, using CPU")
except Exception as e:
    print("GPU disable warning:", e)

from PIL import Image, ImageChops
from io import BytesIO
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from threading import Thread, Lock
from time import sleep

# import os, certifi
# os.environ["SSL_CERT_FILE"] = certifi.where()

# import ssl
# # ssl._create_default_https_context = ssl._create_unverified_context
# truststore.inject_into_ssl()

global status

progress = {}
results = {}
lock = Lock()

def set_progress(job_id, pct, phase):
    with lock:
        progress[job_id] = {"pct": int(pct), "phase": phase}

def set_result(job_id, payload):
    with lock:
        results[job_id] = payload

def get_progress(job_id):
    with lock:
        return progress.get(job_id, {"pct": 0, "phase": "Starting..."})

def get_result(job_id):
    with lock:
        return results.get(job_id)

# ========== LOAD ENV ==========
load_dotenv()

# ========== CONFIG BASIC ==========
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
MAX_CONTENT_LENGTH_MB = int(os.getenv("MAX_CONTENT_LENGTH_MB", "200"))

ALLOWED_IMAGE_EXT = {"jpg", "jpeg", "png"}
ALLOWED_VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXT | ALLOWED_VIDEO_EXT

MODEL_PATH = os.getenv("MODEL_PATH", "model/best_xception_ela.h5")

# ========== FLASK APP SETUP ==========
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH_MB * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app, resources={r"/api/*": {"origins": "*"}})

# db = SQLAlchemy(app)
# jwt = JWTManager(app)
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
print("Model loaded:", MODEL_PATH)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========== MODELS (DATABASE TABLES) ==========
# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
#     password_hash = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             "created_at": self.created_at.isoformat() + "Z",
#         }

# with app.app_context():
#     db.create_all()

# ========== HELPER FUNCTIONS ==========
def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def stub_predict_score_fake(file_path: str) -> float:
    """
    STUB MODEL – sementara belum pakai model beneran.
    Di sini kita pakai hash dari file → jadi angka 0..1.
    Nanti cukup ganti fungsi ini dengan model Xception teman kamu.
    """
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        h.update(f.read(1024 * 1024))  # baca 1MB pertama

    # ambil beberapa digit hash → ubah ke 0..1
    val = int(h.hexdigest()[:8], 16)  # 32-bit int
    return (val % 10_000) / 10_000.0

from tensorflow.keras.applications.xception import preprocess_input

model_lock = Lock()  # biar aman dipanggil dari thread

def preprocess_ela_pil_to_batch(ela_img: Image.Image):
    """
    ELA PIL -> numpy batch (1,299,299,3) + preprocess_input Xception
    Sesuai training notebook: preprocess_input, size 299x299
    """
    img = ela_img.convert("RGB").resize((299, 299))
    x = np.array(img, dtype=np.float32)  # shape (299,299,3), range 0..255
    x = np.expand_dims(x, axis=0)        # (1,299,299,3)
    x = preprocess_input(x)              # Xception preprocess (sesuai notebook)
    return x

def predict_real_fake_from_ela(ela_img: Image.Image):
    """
    Return (real_prob, fake_prob).
    Karena class_indices: fake=0, real=1, maka output sigmoid = P(real)
    """
    x = preprocess_ela_pil_to_batch(ela_img)

    with model_lock:
        pred = model.predict(x, verbose=0)

    # pred biasanya shape (1,1) karena binary_crossentropy + sigmoid
    real_prob = float(pred[0][0])
    real_prob = max(0.0, min(1.0, real_prob))
    fake_prob = 1.0 - real_prob
    return real_prob, fake_prob

def ela_from_image_path(image_path: str):
    """
    Buat ELA image dari file foto.
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(TARGET_SIZE, Image.BICUBIC)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    buf.seek(0)

    recompressed = Image.open(buf).convert("RGB")
    diff = ImageChops.difference(img, recompressed)

    diff_np = np.asarray(diff).astype(np.float32)
    p = np.percentile(diff_np, PERCENTILE)
    p = max(p, EPS)

    diff_np = np.clip(diff_np * (255.0 / p), 0, 255)
    ela_img = Image.fromarray(diff_np.astype(np.uint8))
    return ela_img


TARGET_SIZE = (299, 299)
FRAME_INTERVAL = 30
JPEG_QUALITY = 90
PERCENTILE = 99.0
EPS = 1e-6

def ela_percentile_from_frame(frame_bgr):
    img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    img = img.resize(TARGET_SIZE, Image.BICUBIC)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    buf.seek(0)

    recompressed = Image.open(buf)
    diff = ImageChops.difference(img, recompressed)

    diff_np = np.asarray(diff).astype(np.float32)
    p = np.percentile(diff_np, PERCENTILE)
    p = max(p, EPS)

    diff_np = np.clip(diff_np * (255.0 / p), 0, 255)
    ela_img = Image.fromarray(diff_np.astype(np.uint8))

    return ela_img

def extract_strongest_ela_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    best_score = -1
    best_ela = None

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % FRAME_INTERVAL == 0:
            ela_img = ela_percentile_from_frame(frame)
            score = np.asarray(ela_img).mean()  # intensitas ELA

            if score > best_score:
                best_score = score
                best_ela = ela_img

        frame_idx += 1

    cap.release()

    if best_ela is None:
        raise RuntimeError("No ELA frame extracted")

    return best_ela

# ========== ROUTES ==========
@app.get("/api/health")
def health():
    """Cek server hidup."""
    return jsonify({"status": "ok"})

@app.get("/api/debug/progress")
def debug_progress():
    return jsonify({
        "progress_len": len(progress),
        "job_ids": list(progress.keys())[:10]
    })

# # ---------- AUTH: REGISTER ----------
# @app.post("/api/auth/register")
# def register():
#     data = request.get_json(silent=True) or {}
#     email = (data.get("email") or "").strip().lower()
#     password = data.get("password") or ""

#     if not email or not password:
#         return jsonify({"error": "email dan password wajib diisi"}), 400
#     if len(password) < 6:
#         return jsonify({"error": "password minimal 6 karakter"}), 400

#     # cek sudah register?
#     if User.query.filter_by(email=email).first():
#         return jsonify({"error": "email sudah terdaftar"}), 409

#     # hash password
#     password_hash = generate_password_hash(password)
#     user = User(email=email, password_hash=password_hash)
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "register sukses", "user": user.to_dict()}), 201


# ---------- AUTH: LOGIN ----------
# @app.post("/api/auth/login")
# def login():
#     data = request.get_json(silent=True) or {}
#     email = (data.get("email") or "").strip().lower()
#     password = data.get("password") or ""

#     if not email or not password:
#         return jsonify({"error": "email dan password wajib diisi"}), 400

#     user = User.query.filter_by(email=email).first()
#     if not user or not check_password_hash(user.password_hash, password):
#         return jsonify({"error": "email / password salah"}), 401

#     # buat JWT token
#     access_token = create_access_token(identity=str(user.id))

#     return jsonify({
#         "access_token": access_token,
#         "user": user.to_dict()
#     })


# # ---------- GET: VIEW ALL USERS ----------
# @app.get("/api/users")
# #@jwt_required()  # bisa diakses hanya user yang login
# def get_users():
#     """
#     Balikin semua user (id, email, created_at).
#     Tidak mengembalikan password.
#     """
#     users = User.query.order_by(User.id.asc()).all()
#     return jsonify([u.to_dict() for u in users])

# Proses berat ditaronya di background thread
def run_job(job_id, save_path):
    try:
        set_progress(job_id, 0, "Preparing...")

        # 0–20% (dummy)
        set_progress(job_id, 10, "Extracting frames...")
        sleep(1)
        set_progress(job_id, 20, "Frames ready.")

        # 20–50% ELA
        set_progress(job_id, 30, "Running ELA...")

        ext = os.path.splitext(save_path)[1].lower().replace(".", "")
        is_video = ext in {"mp4", "mov", "avi", "mkv", "webm"}

        if is_video:
            ela_img = extract_strongest_ela_frame(save_path)
        else:
            ela_img = ela_from_image_path(save_path)

        buf = BytesIO()
        ela_img.save(buf, format="PNG")
        ela_bytes = buf.getvalue()

        set_progress(job_id, 50, "ELA completed.")

        # 50–90% Xception
        set_progress(job_id, 65, "Analyzing using detection model...")
        real_prob, fake_prob = predict_real_fake_from_ela(ela_img)
        set_progress(job_id, 90, "Model prediction ready.")

        # 90–100% Gemini explanation (optional)
        set_progress(job_id, 95, "Generating explanation...")

        response_text = ""
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
        
            model_gemini = genai.GenerativeModel("gemma-3-27b-it")
            response = model_gemini.generate_content(
                [
                    {"mime_type": "image/png", "data": ela_bytes},
                    "This project analyzes deepfake detection using ELA (Error Level Analysis) and XceptionNet. "
                    "The image is an ELA result frame. Analyze the ELA image and write exactly one concise paragraph "
                    "in plain text (no bold, italics, headings, or formatting). "
                    "Do not include any introductory or meta sentences."
                ]
            )
            response_text = (response.text or "").strip()
        
        except Exception as e:
            response_text = f"(Gemini explanation failed: {e})"

        set_progress(job_id, 100, "Finalizing...")

        fake_pct = round(fake_prob * 100, 2)
        real_pct = round(real_prob * 100, 2)
        label = "REAL" if real_prob >= 0.5 else "FAKE"

        set_result(job_id, {
            "real_pct": real_pct,
            "fake_pct": fake_pct,
            "label": label,
            "response": response_text,
            "ela_image_b64": base64.b64encode(ela_bytes).decode("utf-8")
        })

    except Exception as e:
        set_result(job_id, {
            "error": True,
            "message": str(e),
            "trace": traceback.format_exc()
        })
    finally:
        try:
            os.remove(save_path)
        except OSError:
            pass

# ---------- POST: UPLOAD & PREDICT ----------
@app.post("/api/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"error": "file missing"}), 400

    f = request.files["file"]
    if not allowed_file(f.filename):
        return jsonify({"error": "invalid format"}), 400
    
    if not f.filename:
        return jsonify({"error": "filename empty"}), 400

    name = secure_filename(f.filename)
    path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{name}")
    f.save(path)

    job_id = uuid.uuid4().hex
    set_progress(job_id, 1, "Queued...")

    Thread(target=run_job, args=(job_id, path), daemon=True).start()
    return jsonify({"job_id": job_id}), 202



#     try:
#         # panggil "model"
#         score_fake = stub_predict_score_fake(save_path)  # 0..1
#         score_fake = max(0.0, min(1.0, float(score_fake)))  # clamp

#         fake_pct = round(score_fake * 100, 2)
#         real_pct = round((1.0 - score_fake) * 100, 2)

#         return jsonify({
#             "job_id": job_id,
#             "real_pct": real_pct,
#             "fake_pct": fake_pct,
#             "label": "FAKE" if score_fake >= 0.5 else "REAL",
#             "response": response.text
#         })
#     finally:
#         with progress_lock:
#             progress.pop(job_id, None)
#         # hapus file
#         try:
#             os.remove(save_path)
#         except OSError:
#             pass

# status = None

# def task():
#     global status
#     for i in range(1,11):
#         status = i
#         sleep(1)

# @app.route('/api/')
# def index():
#     # t1 = Thread(target=task)
#     # t1.start()
#     task()
#     return jsonify({"status": "ok"})

@app.get("/api/status/<job_id>")
def status(job_id):
    return jsonify(get_progress(job_id))

@app.get("/api/result/<job_id>")
def result(job_id):
    r = get_result(job_id)
    if not r:
        return jsonify({"ready": False}), 202
    
    with lock:
        progress.pop(job_id, None)
        results.pop(job_id, None)

    return jsonify({"ready": True, **r})

if __name__ == "__main__":
    # ganti port di sini kalau 5000 bentrok (misal ke 5001)
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)


