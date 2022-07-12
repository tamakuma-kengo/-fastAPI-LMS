<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <CourseInfoBarVue :select_id="3" :course_id="this.course_id"></CourseInfoBarVue>
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
import CourseInfoBarVue from "../../modules/CourseInfoBar.vue";

export default {
  name: "Home",
  props: {
    course_id: Number
  },
  components: {
    CourseInfoBarVue,
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
