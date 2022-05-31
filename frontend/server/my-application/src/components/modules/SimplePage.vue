<template>
    <v-container>
          <div v-html="markdownToHtml(page_content.content)"></div>
    </v-container>
</template>

<script>
// import axios from "axios";
import { marked } from 'marked';

export default {
  name: "SimplePage",
  props: {
    page_content: Object
  },
  mounted() {
   window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  created: function() {
    window.MathJax.Hub.Config({
      tex2jax:{
        extensions: ["tex2jax.js", "TeX/boldsymbol.js"],
        messageStyle: "none",
        inlineMath: [['$','$'],['\\(','\\)']],
        displayMath: [['$$','$$'],['\\[','\\]']],
        processEscapes: true
      }
    });
   window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  data: () => ({
  }),
  methods:{
      markdownToHtml(md){
        return marked(md);
      },
  },
};
</script>
