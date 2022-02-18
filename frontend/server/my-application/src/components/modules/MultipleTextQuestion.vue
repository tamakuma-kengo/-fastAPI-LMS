<template>
    <v-container>
      <v-responsive :min-height="300">
        <v-container>
          <div v-html="markdownToHtml(page_content.content)"></div>
        </v-container>
      </v-responsive>
      <v-container>
        <row v-for="answer_column in this.replaced_answer_columns" :key=answer_column.data>
          <div v-html="markdownToHtml(answer_column.data)" v-if="answer_column.type=='md'"></div>
          <v-text-field
            v-if="answer_column.type=='blank'"
            label="解答を入力"
            v-model= "blank_values[answer_column.data]"
            filled
          ></v-text-field>
        </row>
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
  name: "MultipleTextQuestion",
  props: {
    flow_session_id: Number,
    page_num: Number,
    page_content: Object
  },
  created: function() {
    this.parse_md()
  },
  data: () => ({
    blank_values: {},
    replaced_answer_columns: []
  }),
  methods:{
    markdownToHtml(md){
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
      for (const blank_id in this.blank_values){
        params.push({
          "flow_session_id": this.flow_session_id,
          "page_num": this.page_num,
          "blank_id": blank_id,
          "answer": this.blank_values[blank_id]
        })
      }
      console.log(params)
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
    },
    update_value(aaa){
      console.log(aaa)
    }
  },
};
</script>
