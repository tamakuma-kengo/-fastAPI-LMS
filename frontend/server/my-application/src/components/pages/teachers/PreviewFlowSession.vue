<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-subheader :class="['text-h5']">{{course.course_name}}</v-subheader>
          </v-col>
          <v-col cols="6">
            <v-container>  
              <v-row justify="end">
                <div>
                  {{this.user_info.username}} ( {{this.user_info.email}})<br>
                  {{this.user_info.kind_name}} としてログイン中
                </div>
              </v-row>
              <v-row justify="end">
                <v-btn text color="red" @click="logout()" value="POST">ログアウト</v-btn>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
        <v-row>
        <v-col cols="2">
          <v-btn @click="move_to_course_info()" depressed block color="transparent"  class="mb-2"> 
            コース情報
          </v-btn>
        </v-col>
        <v-col cols="2">
          <v-btn @click="move_to_course_taking()" depressed block color="transparent"  class="mb-2">
            履修者
          </v-btn>
        </v-col >  
        <v-col cols="2">
          <v-btn @click="move_to_course_preview()" depressed block color="transparent"  class="mb-2">
            プレビュー
          </v-btn>
          <v-divider class="red"></v-divider>
        </v-col >  
        <v-col cols="2">
          <v-btn @click="move_to_course_edit()" depressed block color="transparent"  class="mb-2">
            編集
          </v-btn>
        </v-col>  
        </v-row>
        <v-divider class="mt-0"></v-divider>
        <br>
        <v-row class="mt-5">
        <v-subheader :class="['text-h5']">{{this.flow_title}}</v-subheader>
          <v-container>
            <flow-session-location-bar :page_num='this.page_num' :flow_session_id="this.flow_session_id" :num_of_pages="this.num_of_pages"></flow-session-location-bar>
          </v-container>
          <v-subheader :class="['text-h5']">問題{{page_num}}</v-subheader>
          <v-responsive :min-height="600">
            <v-container fluid>
                <component :is="componentName" :page_content='page_content' :flow_session_id='flow_session_id' :page_num='page_num' :blank_answers="blank_answers"></component>
            </v-container>
          </v-responsive>
          <v-container >
            <v-row>
              <v-col>
                <v-btn @click="go_previous_page()" v-if="this.page_num > 1"> 前のページ  </v-btn>
              </v-col>
              <v-col class="d-flex align-end flex-column">
                <v-btn @click="go_next_page()" v-if="this.page_num < this.num_of_pages"> 次のページ </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-row>
      </v-container>
    </v-responsive>
  </v-container>
</template>


<script>
import axios from "axios";
import SimplePage from '../../modules/SimplePage.vue'
import SingleTextQuestion from '../../modules/SingleTextQuestion.vue'
import MultipleTextQuestion from '../../modules/MultipleTextQuestion.vue'
import DescriptiveTextQuestion from '../../modules/DescriptiveTextQuestion.vue'
import ChoiceQuestion from '../../modules/ChoiceQuestion.vue'
import FlowSessionLocationBar from '../../modules/FlowSessionLocationBar.vue'

export default {
  name: "PreviewFlowSession",
  props: {
    course_id: Number,
    flow_session_id: Number,
    page_num: Number,
  },
  components: {
    SimplePage,
    SingleTextQuestion,
    MultipleTextQuestion,
    DescriptiveTextQuestion,
    ChoiceQuestion,
    FlowSessionLocationBar,
  },
  created: function() {
    this.get_flow_info()
    this.update_data()
  },
  data: () => ({
    flow_title: "",
    num_of_pages: 1,
    page: {"title":""},
    page_content: {},
    user_info : {},
    is_creater : false,
    componentName: "",
    blank_answers: [],
    course: {},
  }),
  beforeRouteUpdate (to, from, next) {
    this.update_data()
    next();
  },
  methods:{
    get_flow_info(){
      let self = this
      axios.get(`http://localhost:8000/get_flow_info/${this.flow_session_id}`, {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.flow_title = response.data.flow_title
        self.num_of_pages = response.data.num_of_pages
      }).catch(function(error){
        console.log(error)
      })
    },
    update_data(){
      let self = this
      axios.get("http://localhost:8000/home_profile", {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.user_info = response.data
        self.is_creater = response.data.create
        axios.get(`http://localhost:8000/get_flowpage/${self.flow_session_id}/${self.page_num}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.page = response.data
          self.page_content = response.data.page_content
          self.componentName = response.data.page_type
        }).catch(function(error){
          console.log(error.response)
        })
        axios.get(`http://localhost:8000/get_blank_answer/${self.flow_session_id}/${self.page_num}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.blank_answers = response.data
        }).catch(function(error){
          console.log(error.response)
        })
        }).catch(function(error)  {
          if(error.response.status == 401){
            self.$router.push({name:'Signup'})
          }else{
            console.log(error.response)
          }
        })
    },
    go_previous_page(){
      this.$router.push({name:'PreviewFlowSession', params: {flow_session_id: this.flow_session_id, page_num: this.page_num-1, blank_answers: this.blank_answers}})
    },
    go_next_page(){
      this.$router.push({name:'PreviewFlowSession', params: {flow_session_id: this.flow_session_id, page_num: this.page_num+1, blank_answers: this.blank_answers}})
    },
    get_course_info(){
      let self = this
      axios.get(`http://localhost:8000/get_course_info/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.course = response.data
        }).catch(function(error){
          console.log(error.response)
        }).catch(function(error)  {
          if(error.response.status == 401){
            self.$router.push({name:'Signup'})
          }else{
            console.log(error.response)
          }
        }
      ) 
    },
  },
};
</script>
