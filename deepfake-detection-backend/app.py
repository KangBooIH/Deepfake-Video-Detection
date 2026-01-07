import os
import uuid
import traceback
import cv2
import numpy as np
import base64
import tensorflow as tf

# ===== Force CPU (stabil untuk Mac) =====
try:
    tf.config.set_visible_devices([], "GPU")
except:
    pass

from PIL import Image, ImageChops
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from threading import Thread, Lock
from time import sleep
from dotenv import load_dotenv

from tensorflow.keras.applications.xception import preprocess_input

# ================= ENV =================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ================= CONFIG =================
UPLOAD_FOLDER = "uploads"
MODEL_PATH = "model/best_xception_ela.h5"

TARGET_SIZE = (299, 299)
FRAME_INTERVAL = 30
JPEG_QUALITY = 90
PERCENTILE = 99.0
EPS = 1e-6

ALLOWED_EXT = {"jpg", "jpeg", "png", "mp4", "mov", "avi", "mkv", "webm"}

# ================= APP =================
app = Flask(__name__)
CORS(app)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
model_lock = Lock()

progress = {}
results = {}
lock = Lock()

# ================= UTIL =================
def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def set_progress(job_id, pct, phase):
    with lock:
        progress[job_id] = {"pct": pct, "phase": phase}

def set_result(job_id, data):
    with lock:
        results[job_id] = data

# ================= ELA =================
def ela_from_frame(frame_bgr):
    img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    img = img.resize(TARGET_SIZE, Image.BICUBIC)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    buf.seek(0)

    recompressed = Image.open(buf)
    diff = ImageChops.difference(img, recompressed)

    diff_np = np.asarray(diff).astype(np.float32)
    p = max(np.percentile(diff_np, PERCENTILE), EPS)
    diff_np = np.clip(diff_np * (255.0 / p), 0, 255)

    return Image.fromarray(diff_np.astype(np.uint8))

# ================= MODEL =================
def predict_from_ela(ela_img):
    x = np.expand_dims(np.array(ela_img.convert("RGB")), axis=0)
    x = preprocess_input(x.astype(np.float32))

    with model_lock:
        pred = model.predict(x, verbose=0)

    real = float(pred[0][0])
    fake = 1.0 - real
    return real, fake

# ================= VIDEO =================
def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    real_probs, fake_probs = [], []
    best_ela, best_score = None, -1
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % FRAME_INTERVAL == 0:
            ela_img = ela_from_frame(frame)
            score = np.asarray(ela_img).mean()

            if score > best_score:
                best_score = score
                best_ela = ela_img

            r, f = predict_from_ela(ela_img)
            real_probs.append(r)
            fake_probs.append(f)

        idx += 1

    cap.release()

    mean_real = float(np.mean(real_probs))
    mean_fake = float(np.mean(fake_probs))
    label = "REAL" if mean_real >= 0.5 else "FAKE"

    return mean_real, mean_fake, label, best_ela

# ================= GEMINI =================
def explain_with_gemini(ela_bytes):
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel("gemma-3-27b-it")
        resp = model.generate_content([
            {"mime_type": "image/png", "data": ela_bytes},
            "Explain in one concise paragraph why this ELA image indicates a real or fake video. "
            "No intro, no formatting."
        ])
        return resp.text.strip()
    except Exception as e:
        return f"(AI explanation unavailable: {e})"

# ================= JOB =================
def run_job(job_id, path):
    try:
        set_progress(job_id, 10, "Processing video...")
        real, fake, label, ela_img = analyze_video(path)

        buf = BytesIO()
        ela_img.save(buf, format="PNG")
        ela_bytes = buf.getvalue()

        set_progress(job_id, 80, "Generating explanation...")
        explanation = explain_with_gemini(ela_bytes)

        set_progress(job_id, 100, "Done")

        set_result(job_id, {
            "real_pct": round(real * 100, 2),
            "fake_pct": round(fake * 100, 2),
            "label": label,
            "response": explanation,
            "ela_image_b64": base64.b64encode(ela_bytes).decode()
        })

    except Exception as e:
        set_result(job_id, {
            "error": True,
            "message": str(e),
            "trace": traceback.format_exc()
        })
    finally:
        try:
            os.remove(path)
        except:
            pass

# ================= ROUTES =================
@app.post("/api/predict")
def predict():
    f = request.files.get("file")
    if not f or not allowed_file(f.filename):
        return jsonify({"error": "invalid file"}), 400

    name = secure_filename(f.filename)
    path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{name}")
    f.save(path)

    job_id = uuid.uuid4().hex
    set_progress(job_id, 1, "Queued")

    Thread(target=run_job, args=(job_id, path), daemon=True).start()
    return jsonify({"job_id": job_id}), 202

@app.get("/api/status/<job_id>")
def status(job_id):
    return jsonify(progress.get(job_id, {"pct": 0, "phase": "Waiting"}))

@app.get("/api/result/<job_id>")
def result(job_id):
    r = results.get(job_id)
    if not r:
        return jsonify({"ready": False}), 202

    progress.pop(job_id, None)
    results.pop(job_id, None)
    return jsonify({"ready": True, **r})

@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200

# ================= MAIN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
