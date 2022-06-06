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
        <v-row v-for="block in this.course.blocks" :key="block.order">
          <div v-html="markdownToHtml(block.content)"></div>
        </v-row>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "Home",
  props: {
    course_id: Number
  },
  created: function() {
    let self = this
    window.MathJax.Hub.Config({
      tex2jax:{
        extensions: ["tex2jax.js", "TeX/boldsymbol.js"],
        messageStyle: "none",
        inlineMath: [['$','$'],['\\(','\\)']],
        displayMath: [['$$','$$'],['\\[','\\]']],
        processEscapes: true
      }
    })
    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.user_info = response.data
          self.is_creater = response.data.create
          axios.get(`http://localhost:8000/get_course/${self.course_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.course = response.data
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
          if(self.is_creater){
            self.get_course_info()
          }
        }).catch(
          function(error)  {
            console.log(error)
            if(error.response.status == 401){
              self.$router.push({name:'Signup'})
            }else{
              console.log(error.response)
            }
          }
        )
  },
  data: () => ({
    tab: null,
    user_info : {},
    is_create : false,
    course: {},
  }),
  mounted() {
    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  methods:{
    markdownToHtml(md){
      return marked(md);
    },
    logout: function(){
      try{
        const res = axios.post("http://localhost:8000/logout",{},{withCredentials: true})
        console.log(res.data)
        this.moveToLogin()
      }catch(error){
        const {status,statusText} = error.response;
        if(status == 401)
          this.moveToLogin()
        console.log(status,statusText)
      }
    },
    moveToLogin: function(){
      this.$router.push({name:'Login'})
    },
    move_to_course_info(){
      this.$router.push({name:'CourseInfo', params:{"course_id":this.course_id}})
    },
    move_to_course_taking(){
      this.$router.push({name:'CourseTaking',params:{"course_id":this.course_id}})
    },
    move_to_course_preview(){
      this.$router.push({name:'CoursePreview',params:{"course_id":this.course_id}})
    },
    move_to_course_edit(){
      this.$router.push({name:'CourseEdit',params:{"course_id":this.course_id}})
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
    }
  },
};
</script>
