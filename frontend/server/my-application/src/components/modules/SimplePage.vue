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
  created: function() {
    
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
