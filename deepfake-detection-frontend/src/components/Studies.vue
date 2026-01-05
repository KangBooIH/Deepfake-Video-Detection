<template>
    <div id="allStudies">
        <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }">
            <h1 id="About">The Study That Powers Our Detection System</h1>
        </div>
        <div class="ELAsection">
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-l-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="videoStudiesELA">
                <video class="ELAvideo" autoplay loop muted>
                    <source src="../vid/ELAwebasset.mp4">
                </video>
            </div>
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-r-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="ELAtext">
                <h2 class="subTitle2">Error Level Analysis</h2>
                <h3>A Digital Forensics Technique for Revealing Visual Manipulation</h3>
                <p>Before applying ELA, the uploaded video is first converted into individual frames. This step is important because ELA works at the image level, each frame must be analyzed separately to detect subtle manipulation patterns that appear across the video.</p>
                <p>Error Level Analysis (ELA) is a digital forensics method used to identify signs of manipulation by examining inconsistencies in JPEG compression. Original images typically have uniform compression, while edited regions produce different error levels that can reveal traces of tampering.</p>
                <h3>How ELA Works</h3>
                <ul>
                    <li>The image or video frame is resaved with a fixed compression quality.</li>
                    <li>The system calculates pixel-by-pixel differences between the original frame and the recompressed version.</li>
                    <li>Unaltered areas typically appear darker, indicating consistent compression.</li>
                    <li>Manipulated areas appear brighter, showing significant compression differences.</li>
                    <li>The results are visualized as a heatmap, highlighting suspicious regions.</li>
                    <br>
                </ul>
                <h3>Why We Use ELA</h3>
                <p>ELA enhances subtle manipulation cues that are often invisible to the human eye.</p>
                <p>By processing every video frame through ELA, the system produces clearer patterns of compression inconsistency, making it easier for the deep learning model to recognize signs of deepfake manipulation and achieve more accurate predictions.</p>
            </div>
        </div>
        <div class="xceptionSection">
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-l-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="xceptionText">
                <h2>XceptionNet</h2>
                <h3>A Deep Learning Model for High-Accuracy Deepfake Detection</h3>
                <p>XceptionNet is a deep learning architecture designed to extract complex visual patterns efficiently. The model uses depthwise separable convolutions, allowing it to learn detailed features from images or video frames while keeping computation lightweight. This makes XceptionNet highly effective for detecting subtle manipulation artifacts commonly found in deepfake content.</p>
                <h3>How XceptionNet Works</h3>
                <ul>
                    <li>Heatmaps from the ELA preprocessing step are resized and normalized to fit XceptionNet's input format.</li>
                    <li>The model processes these images through stacked convolutional layers to extract spatial features.</li>
                    <li>Extracted features are passed to fully connected layers to classify each frame as real or fake.</li>
                    <li>Pretrained ImageNet weights are used to provide strong initial feature-learning ability, followed by fine-tuning for deepfake-specific patterns.</li>
                    <br>
                </ul>
                <h3>Why We Use XceptionNet</h3>
                <p>XceptionNet is known for its high accuracy in visual classification tasks and has shown strong performance in detecting deepfake manipulations, even in heavily compressed videos. Its architecture allows the system to identify subtle inconsistencies that traditional CNNs often miss, making it a reliable backbone for deepfake detection.</p>
            </div>
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-r-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="imageStudiesXception">
                <img class="xceptionImage" src="../img/Proposed-structure-of-Xception-network-used-within-each-stream-of-CNN.jpg" alt="">
            </div>
        </div>

        <div class="resultsSection">
            <h1 v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }">Powered by Research, Proven by Results</h1>
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-r-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="imageResults">
                <img class="matrix" src="" alt="">
            </div>
            <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-l-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="resultsText">
                <p style="text-align: center;">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi dignissimos, repudiandae repellendus at nihil fugit, incidunt accusamus quas blanditiis porro facere ducimus ea. Unde necessitatibus vel incidunt autem praesentium molestias.</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
#allStudies {
    padding: 6rem 5rem 0 5rem;
    width: 100%;
}

h1 {
    font-weight: bold;
    font-size: 45px;
    /*position: absolute;*/
    /* top: -10px; */
    color: #ffffff;
    text-align: center;
}

/* .studiesVisualAssets {
    display: flex; 
    flex-direction: column;
    align-items: center;
    justify-content: center;
} */

.ELAsection {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-top: 2rem;
}

.ELAvideo {
    margin-top: 0rem;
    width: 100%;
    border-radius: 20px;
}

.videoStudiesELA {
  width: 50%;
  /* margin-right: 2%; */
}

.ELAtext {
    width: 45%;
    padding: 0.5rem;
}

.xceptionSection {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-top: 3rem;  /* Memberikan jarak antara ELA dan Xception */
}

.xceptionImage {
    margin-top: 0rem;
    width: 100%;
    border-radius: 20px;
}

.imageStudiesXception {
  width: 50%;
  /* margin-right: 2%; */
}

.xceptionText {
    width: 45%;
    padding: 1rem;
}

h2 {
    font-weight: 700;
    font-size: 35px;
    color: #ffffff;    
}

p, li, h3 {
    color: #ffffff;
    font-size: 1rem;
    text-align: justify;;
}

p {
    margin-bottom: 2rem;
}

ul {
    list-style-type: disc;
    padding-left: 2rem;
}

h3 {
    font-weight: 680;
    font-size: 20px;
}

.resultsSection {
    padding: 5rem 5rem 0 5rem;
    width: 100%;
    align-items: center;
}

/* .presults {
    text-align: center;
} */

</style>