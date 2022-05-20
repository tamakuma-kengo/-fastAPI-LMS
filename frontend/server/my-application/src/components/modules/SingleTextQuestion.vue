<template>
    <v-container fluid class="pa-0">
      <v-responsive :min-height="300">
        <v-container fluid >
          <div v-html="markdownToHtml(page_content.content)"></div>
        </v-container>
      </v-responsive>
      <v-container class="pa-0">
        <div :class="`rounded-lg`" class="pa-8 grey lighten-3 text-no-wrap">
          <v-row>
            <v-text-field
                label="回答を入力"
                background-color="white"
                v-model="blank_answer[page_content.blank_id]"
                filled
              ></v-text-field>
          </v-row>
          <v-row align="end" justify="end">
            <v-btn @click="register_answer()" color="primary" width="100"> 回答する </v-btn>

          </v-row>
        </div>
      </v-container>
      <v-container class="pa-0 mt-4">
        <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap" v-if="is_correct=='正解です！！'">
          <v-row>
            {{is_correct}}
          </v-row>
        </div>
        <div :class="`rounded-lg`" class="pa-6 mt-6 red lighten-5 text-no-wrap" v-if="is_correct=='不正解です'">
          <v-row>
            {{is_correct}}
          </v-row>
          <v-row>
            解説：数列の和の公式を確認しよう！！
          </v-row>
        </div>
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
    blank_answer: {},
    is_correct: "",
    is_registered: {},
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
        "answer": this.blank_answer[this.page_content.blank_id],
        "is_correct": this.is_correct
      }]
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      let self = this
      axios.post(`http://localhost:8000/register_blank_answer`, params, config)
      .then(function(response){
        console.log(response.data)
        self.is_correct = ""
        if(response.data[0]["is_correct"] == true){
          self.is_correct='正解です！！'
        }else{
          self.is_correct='不正解です'
        }
      }).catch(
        function(error){
          console.log(error)
        }
      )
    }
  },
};
</script>