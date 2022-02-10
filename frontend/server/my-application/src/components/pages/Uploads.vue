<template>
<div id="app">
    <input id="image" v-on:change="onFileChange" type="file" webkitdirectory>
</div>
</template>
<style>
/*
import '~vue-upload-component/dist/vue-upload-component.part.css'
@import "~vue-upload-component/dist/vue-upload-component.part.css";

或


 */
.file-uploads {
  overflow: hidden;
  position: relative;
  text-align: center;
  display: inline-block;
}
.file-uploads.file-uploads-html4 input[type="file"] {
  opacity: 0;
  font-size: 20em;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  position: absolute;
  width: 100%;
  height: 100%;
}
.file-uploads.file-uploads-html5 input[type="file"] {
  overflow: hidden;
  position: fixed;
  width: 1px;
  height: 1px;
  z-index: -1;
  opacity: 0;
}
</style>
<script>
export default {
  data() {
    return {
      files: []
    }
  },
  methods: {
    onFileChange(fileObjects) {
      const files = fileObjects.target.files;
      
      for(let file of files){
        let filePath = file.webkitRelativePath
        console.log(filePath)
        let fileReader = new FileReader();
        fileReader.onload = event => {
          let text = event.target.result;
          console.log(text );
        }
        fileReader.readAsText(file);
      }

    },
  }
}
</script>