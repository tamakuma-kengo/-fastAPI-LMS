<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-banner height="100" :class="['text-h5']">{{course.course_name}}
          <v-row justify="end">
            <v-btn text color="grey" @click="logout()" value="POST">logout</v-btn>
          </v-row>
        </v-banner>
        <v-container>
          <v-row v-for="block in this.course.blocks" :key="block.order">
            <div v-html="markdownToHtml(block.content)"></div>
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
  name: "Course",
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
          self.username = response.data.username
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
    course: {},
    username : "",
    is_creater : false,
    html: "# aaaaa",
    markdown:  "# Hello World",
  }),
  mounted() {
   window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
  },
  methods:{
      add_course(){
        this.$router.push({name:'RegisterCourse'})
      },
      markdownToHtml(md){
        return marked(md);
      },
      logout: function(){
        let self = this
        axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          if(response.data.is_active){
            self.go_login_page()
          }
        }).catch(
          function(error){
            console.log(error)
            if(error.response.status == 401){
              self.$router.push({name:'Login'})
            }else{
              console.log(error.response)
            }
          }
        )
      },
      go_login_page: function(){
        this.$router.push({name:'Login'})
      }
  },
};
</script>
