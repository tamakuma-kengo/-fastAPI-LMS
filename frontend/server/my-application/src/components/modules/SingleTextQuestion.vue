<template>
    <v-container fluid >
      <v-responsive :min-height="300">
        <v-container fluid >
          <div v-html="markdownToHtml(page_content.content)"></div>
        </v-container>
      </v-responsive>
      <v-container>
        <v-row>
          <v-text-field
              label="解答を入力"
              v-model="blank_answer"
              filled
            ></v-text-field>
        </v-row>
        <v-row align="end" justify="end">
          <v-btn @click="register_answer()" color="primary" width="100"> 解答 </v-btn>
        </v-row>
      </v-container>
    </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "SingleTextQuestion",
  props: {
    flow_session_id: Number,
    page_num: Number,
    page_content: Object
  },
  created: function() {
    
  },
  data: () => ({
    blank_answer: ""
  }),
  methods:{
    markdownToHtml(md){
      return marked(md);
    },
    register_answer(){
      const params = [{
        "flow_session_id": this.flow_session_id,
        "page_num": this.page_num,
        "blank_id": this.page_content.blank_id,
        "answer": this.blank_answer
      }]
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      axios.post(`/api/register_blank_answer`, params, config)
      .then(function(response){
        console.log(response.data)
      }).catch(
        function(error){
          console.log(error)
        }
      )
    }
  },
};
</script>
