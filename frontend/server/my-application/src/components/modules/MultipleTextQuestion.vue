<template>
    <v-container class="pa-0">
      <v-responsive :min-height="300">
        <v-container>
          <div v-html="markdownToHtml(page_content.content)"></div>
        </v-container>
      </v-responsive>
      <v-container class="pa-0">
        <div :class="`rounded-lg`" class="pa-8 grey lighten-3 text-no-wrap"  >
          <v-row v-for="answer_column in this.replaced_answer_columns" :key=answer_column.data>
            <div v-html="markdownToHtml(answer_column.data)" v-if="answer_column.type=='md'"></div>
            <v-text-field
              v-if="answer_column.type=='blank'"
              background-color="white"
              label="解答を入力"
              v-model= "blank_answer[answer_column.data]"
              filled
            ></v-text-field>
          </v-row>
          <v-row align="end" justify="end">
              <v-btn @click="register_answer()" color="primary" width="100"> 解答する </v-btn>
          </v-row>
        </div>
      </v-container>
    </v-container>
</template>
<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "MultipleTextQuestion",
  props: {
    flow_session_id: Number,
    page_num: Number,
    page_content: Object,
    blank_answers: Array,
  },
  watch: {
    page_content: {
      handler: function () {
        this.parse_md()
        this.blank_answer = {}
        this.blank_answers.forEach(ba => {
          this.blank_answer[ba.blank_id] = ba.answer
        });
      },
      deep: true
    }
  },
  mounted() {
   window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  created: function() {
    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);

    this.parse_md()
    this.blank_answers.forEach(ba => {
      this.blank_answer[ba.blank_id] = ba.answer
    });
  },
  data: () => ({
    blank_answer: {},
    blank_values: {},
    replaced_answer_columns: [],
  }),
  methods:{
    markdownToHtml(md){
      window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
      return marked(md);
    },
    parse_md(){
      const md = this.page_content.answer_column_content
      const regexp = /\[\[\s*?.*?\s*?\]\]/g
      const blanks = [...md.matchAll(regexp)]
      console.log(blanks)
      console.log(blanks[0])
      console.log(blanks)

      if (blanks === "undefined") {
        return marked(replaced_md)
      }
      let replaced_md = md
      let replaced_answer_columns = []
      blanks.forEach(blank => {
        let blank_id = blank[0].slice(2,-2)
        this.blank_values[blank_id] = ""
        const splited = replaced_md.split(blank[0])
        replaced_answer_columns.push({"type":"md", "data": splited[0]})
        replaced_answer_columns.push({"type":"blank", "data": blank_id})
        replaced_md = splited[1]
      });
      this.replaced_answer_columns = replaced_answer_columns
      return marked(replaced_md)
    },

    register_answer(){
      const params = []
      for (const blank_id in this.blank_answer){
        params.push({
          "flow_session_id": this.flow_session_id,
          "page_num": this.page_num,
          "blank_id": blank_id,
          "answer": this.blank_answer[blank_id]
        })
      }
      console.log(params)
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
    },
  },
};
</script>
