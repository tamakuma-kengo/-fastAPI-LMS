<template>
    <v-container class="pa-0">
      <v-responsive :min-height="400">
        <v-container>
          <div v-html="markdownToHtml(page_content.content)"></div>
        </v-container>
      </v-responsive>
      <v-container class="pa-0">
        <div :class="`rounded-lg`" class="pa-8 pl-12 grey lighten-3 text-no-wrap"  >
          <v-row>
            <v-radio-group v-model="blank_answer[page_content.blank_id]">
              <v-row v-for="choice in page_content.choices" :key="choice.order">
                <v-radio  :value="choice.id"></v-radio>
                <div v-html="markdownToHtml(choice.content)"></div>
              </v-row>
            </v-radio-group>
          </v-row>
          <v-row align="end" justify="end">
            <v-btn @click="register_answer()" color="primary" width="100"> 回答する </v-btn>
          </v-row>
        </div>
      </v-container>
    </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "ChoiceTextQuetsion",
  props: {
    flow_session_id: Number,
    page_num: Number,
    page_content: Object,
    blank_answers: Array,
  },
  mounted() {
   window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  created: function() {
    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
    this.blank_answers.forEach(ba => {
      this.blank_answer[ba.blank_id] = ba.answer
    });
  },
  data: () => ({
    blank_answer: {}
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
          "answer": this.blank_answer[this.page_content.blank_id]
        }]
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        axios.post(`http://localhost:8000/register_blank_answer`, params, config)
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
