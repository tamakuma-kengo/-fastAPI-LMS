<template>
    <v-container>
      {{this.username}} さん 
      <v-row align="center" justify="space-around" v-if="is_creater">
        <v-btn depressed color="primary" @click="add_course()" value="POST">
          Add Course
        </v-btn>
      </v-row>
      <v-row align="center" justify="space-around" v-if="!is_creater">
        <v-btn depressed color="primary" @click="move_to_courses()" value="POST">
          show courses
        </v-btn>
      </v-row>
    </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  created: function() {
    let self = this
    axios.get("http://127.0.0.1:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.username = response.data.username
          self.is_creater = response.data.create
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
  }),
  methods:{
      add_course(){
        this.$router.push({name:'RegisterCourse'})
      },
      move_to_courses(){
        this.$router.push({name:'Courses'})
      }
  },
};
</script>
