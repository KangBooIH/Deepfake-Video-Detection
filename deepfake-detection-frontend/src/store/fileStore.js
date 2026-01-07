import { defineStore } from "pinia"
import { ref } from 'vue';

export const usefileStore = defineStore('file', () => {
  const file = ref('')
  function setFile(filse){
    file.value = filse
  }

  return { file, setFile }
})