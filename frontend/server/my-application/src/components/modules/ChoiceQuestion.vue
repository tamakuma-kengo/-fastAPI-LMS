<template>
    <v-container>
      <v-responsive :min-height="400">
        <v-container>
          <row>
            <div v-html="markdownToHtml(page_content.content)"></div>
          </row>
        </v-container>
      </v-responsive>
      <v-container>
        <v-row>
          <v-radio-group v-model="blank_answer">
            <v-row v-for="choice in page_content.choices" :key="choice.order">
              <v-radio  :value="choice.id"></v-radio>
              <div v-html="markdownToHtml(choice.content)"></div>
            </v-row>
          </v-radio-group>
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
  name: "ChoiceTextQuetsion",
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
