<script setup>
  import Studies from './Studies.vue';
  import Feedback from './Feedback.vue';
  import { ref } from 'vue';
  import { usefileStore } from '@/store/fileStore';
  import { onMounted } from 'vue';
  import { useRouter } from 'vue-router';

  const isDragging = ref(false)
  const fileInput = ref(null);
  const store = usefileStore()
  const files = ref([])
  const router = useRouter()

  onMounted(() => {
    store.setFile('')
  })

  function dragover(e) {
    e.preventDefault()
    isDragging.value = true
  }

  function dragleave(e) {
    e.preventDefault()
    isDragging.value = false
  }

  function drop(e) {
    e.preventDefault()
    isDragging.value = false

    const dropped = Array.from(e.dataTransfer.files)
    files.value = dropped[0]
    store.setFile(files.value)
    router.push({path: '/upload'})
  }

  function onchange(e) {
    files.value = Array.from(e.target.files)
  }

  function getFile(){
    document.getElementById("getFile").click();
  }

    const handleFileSelect = () => {
      const input = fileInput.value?.files
      if (!input || input.length === 0) return

      const selectedFile = input[0]
      files.value = selectedFile
      store.setFile(selectedFile)
      router.push({ path: '/upload' })
    }
  }

</script>

<template>
  <div>
    <div class="home" id="home" @dragover="dragover" @dragleave="dragleave" @drop="drop">
      <div class="homeVideo">
        <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-l-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" class="centerHomeVideo">
          <video class="theHomeVideo" autoplay muted loop>
            <source src="../vid/01_15__outside_talking_still_laughing__02HILKYO.mp4" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
      <div id="drop-zone" class="homeRightSide">
        <div class="centerRightSide">
          <h1 v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }">Deepfake Video Detector Tool</h1>
  
          <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-r-8 animate-duration-1000', leaveClass: 'animate-leave fade-out-0' }" id="wasdrop-zone">
            <div class="inputFileButton">
              <button class="theFileButton"
                  @click="getFile()"
                  :style="!isDragging && 'pointer-events: auto'">
                Upload your video here!
              </button>

              <input 
                  type="file"
                  accept="video/*"
                  id="getFile"
                  ref="fileInput"
                  style="display: none;"
                  @change="handleFileSelect"
              />
            </div>
            
            <label for="drop-zone" class="file-label">
              <div v-if="isDragging">Release to drop files here.</div>
              <div v-else>or drop files here to upload.</div>
            </label>
            <!-- <ul id="preview"></ul> -->
            <!-- <button id="clear-btn">Clear</button> -->
          </div>
          
        </div>
      </div>
      <div v-if="isDragging">
        <div class="dragging" style="color: #ffffff; font-weight: 700; font-size: 30px;">drop files here to upload</div>
      </div>
    </div>
      <Studies></Studies>
      <Feedback></Feedback>
  </div>
</template>

<style scoped>
h1 {
  font-weight: bold;
  font-size: 45px;
  /*position: absolute;*/
  /* top: -10px; */
  color: #EFDAFF;
  text-align: center;
}

.home {
  /* padding-top: 10rem; */
  padding: 14rem 5rem 13rem 5rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.centerHomeVideo {
    align-items: center;
    display: flex;
    justify-content: center;
}

.theFileButton {
  color: rgb(0, 0, 0);
  padding: 18px;
  top: 10px;
  font-weight: 500;
  border-radius: 50px;
  background-color: #933ace;
  transition: 0.7s;
  cursor: pointer;
  margin-top: 1rem;
  font-size: 16px;
  border: none;
}

.theFileButton:hover {
  background-color: #9714bf;
  box-shadow: 0em 0em 2em rgba(233, 114, 251, 0.665);
  color: rgb(255, 255, 255);
}

.homeVideo {
  width: 50vw;
  display: inline-block;
}

.inputFileButton {
  line-height: normal;
  cursor: auto;
}

.theHomeVideo {
    width: 40vw; 
    border-radius: 60px;
  }
  
.homeRightSide {
    width: 50vw;
    display: inline-block;
    align-items: center;
}

.centerRightSide {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

#wasdrop-zone {
  width: 100%;
  height: 100%;
  margin: 20px auto;
  text-align: center;
  line-height: 50px;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column; 
}

#preview {
  text-align: center;
}

#home * {
    pointer-events: none;
}

.dragging {
  position: fixed;
  border-style: dashed;
  border-color: #EFDAFF;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  /* padding: 10rem; */
  /* margin: 20px auto; */
  text-align: center;
  line-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* flex-direction: column; */
  background-color: #933acead;
  transition: all 0.6s;
}

</style>
