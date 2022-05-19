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
              label="回答を入力"
              v-model= "blank_answer[answer_column.data]"
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
    is_correct: ""
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
      let self = this
      axios.post(`http://localhost:8000/register_blank_answer`, params, config)
      .then(function(response){
        console.log(response.data)
        self.is_correct =""
        self.cnt = 0 // 正解の数をカウント
        for(let i=0; i< response.data.length; i++){
          if(response.data[i]["is_correct"] == true){
            self.cnt ++
          }
        }
        console.log(self.cnt)
        console.log(response.data.length)
        // 全問正解なら正解と表示
        if(response.data.length==self.cnt){
          self.is_correct="正解です！！"
        }else{
          self.is_correct="不正解です"
        }
      }).catch(
        function(error){
          console.log(error)
        }
      )
    },
  },
};
</script>
