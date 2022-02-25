<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-subheader :class="['text-h5']">{{flow_title}}</v-subheader>
        <v-container class="mt-6">
          <v-row>
            <div v-html="markdownToHtml(completion_page_content)"></div>
          </v-row>
          <v-row class="mt-8">
            <v-btn depressed color="primary" @click="move_to_flow_top()">
              フロートップに戻る
            </v-btn>
          </v-row>
        </v-container>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "FlowCompletion",
  props: {
    flow_session_id: Number
  },
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
    .then(function(response){
      console.log(response.data)
      self.get_ids_by_session_id()
      self.get_flow_info()
    }).catch(
      function(error)  {
        if(error.response.status == 401){
          self.$router.push({name:'Login'})
        }else{
          console.log(error.response)
        }
      }
    )
  },
  data: () => ({
    flow: {},
    completion_page_content: "",
    username : "",
    is_creater : false,
    flow_title : "",
    flow_id: null,
    course_id: null,
  }),
  methods:{
    move_to_flow_top(){
      this.$router.push({name:'Flow', params: {course_id:this.course_id, flow_id:this.flow_id}})
    },
    markdownToHtml(md){
      return marked(md);
    },
    get_flow_info(){
      let self = this
      axios.get(`http://localhost:8000/get_flow_info/${this.flow_session_id}`, {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.flow_title = response.data.flow_title
      }).catch(function(error){
        console.log(error)
      })
    },
    get_completion_page(){
      let self = this
      axios.get(`http://localhost:8000/get_flow_completion_page/${self.flow_id}`, {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.completion_page_content= response.data.content
      }).catch(
        function(error){
          console.log(error.response)
        }
      )
    },
    get_ids_by_session_id(){
      let self = this
      axios.get(`http://localhost:8000/get_ids_by_flow_session_id/${self.flow_session_id}`, {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.flow_id = response.data.flow_id
        self.course_id = response.data.course_id
        self.get_completion_page()
      }).catch(function(error){
        console.log(error.response)
      })
    },
  },
};
</script>
