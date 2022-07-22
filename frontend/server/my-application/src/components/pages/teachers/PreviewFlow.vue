<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>

        <CourseInfoBarVue :select_id="3" :course_id="this.course_id"></CourseInfoBarVue>
        <v-row>
          <FlowVue :course_id="this.course_id" :flow_id="this.flow_id"></FlowVue>
        </v-row>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
import FlowVue from "../students/Flow.vue";
import CourseInfoBarVue from "../../modules/CourseInfoBar.vue";

export default {
  name: "PreviewFlow",
  props: {
    course_id: Number,
    flow_id: Number
  },
  components: {
    FlowVue,
    CourseInfoBarVue
},
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.user_info = response.data
          self.is_creater = response.data.create
          axios.get(`http://localhost:8000/get_flow/${self.flow_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.flow = response.data
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
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
    user_info : {},
    is_creater : false,
    markdown:  "# Hello World",
    course: {}
  }),
  methods:{
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
  },
};
</script>
