<template>
    <v-container>
        {{this.username}} さん
        <v-subheader :class="['text-h5']">履修中のコース</v-subheader>
        
      <v-divider></v-divider>
      <v-container tm="24">
        <v-row >
          <v-col cols="12" sm="6" md="4" lg="3" xl="2" v-for="course in this.courses" :key="course.course_name" >
            <v-card @click="start_course(course.course_id)">
              <v-card-text>{{course.course_name}}</v-card-text>
            </v-card>
          </v-col>            
        </v-row>
      </v-container>
    </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Course",
  props: {
    course_id: Number
  },
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.username = response.data.username
          self.is_creater = response.data.create

          axios.get("http://localhost:8000/get_courses", {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.courses = response.data
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
    username : "",
    is_creater : false,
    courses : [
      {"course_name":"aaaa"},
    ]
  }),
  methods:{
      start_course(course_id){
        this.$router.push({name:'Course', params: {course_id: course_id}})
      }
  },
};
</script>
