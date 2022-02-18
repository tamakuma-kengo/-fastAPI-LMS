<template>
    <v-container>
      <v-subheader :class="['text-h5']">{{flow.title}}</v-subheader>
      <v-container>
        <v-row>
          <div v-html="markdownToHtml(welcome_page_content)"></div>
        </v-row>
        <v-row>
          <v-btn depressed color="primary" @click="start_new_flow_session()">
            Start Flow Session
          </v-btn>
        </v-row>
      </v-container>
    </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "Flow",
  props: {
    course_id: Number,
    flow_id: Number
  },
  created: function() {
    let self = this
    axios.get("http://127.0.0.1:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.username = response.data.username
          self.is_creater = response.data.create
          axios.get(`http://127.0.0.1:8000/get_flow/${self.flow_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.flow = response.data
            axios.get(`http://127.0.0.1:8000/get_flow_welcome_page/${self.flow_id}`, {withCredentials: true})
            .then(function(response){
              console.log(response.data)
              self.welcome_page_content = response.data.content
            }).catch(
              function(error){
                console.log(error.response)
              }
            )
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
        }).catch(
          function(error)  {
            if(error.response.status == 401){
              self.$router.push({name:'Signup'})
            }else{
              console.log(error.response)
            }
          }
        )
  },
  data: () => ({
    flow: {},
    welcome_page_content: "",
    username : "",
    is_creater : false,
    html: "# aaaaa",
    markdown:  "# Hello World",
  }),
  methods:{
      markdownToHtml(md){
        return marked(md);
      },
      start_new_flow_session(){
        const params = {"flow_id":this.flow_id}
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        let self = this;
        axios.post(`/api/start_new_flow_session`, params, config)
          .then(function(response){
            console.log(response.data)
            if(response.data.start_success){
              self.$router.push({name:'FlowSession', params: {flow_session_id: response.data.flow_session_id, page_num: 1}})
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
