<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-row justify="end">
          <v-responsive :max-width="300">
            <v-container>
              <v-row>
                {{this.user_info.username}} ( {{this.user_info.email}} )
              </v-row>
              <v-row>
                {{this.user_info.kind_name}} としてログイン中
              </v-row>
            </v-container>
          </v-responsive>
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
          <v-btn depressed block color="transparent"  class="mb-2">
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
        <v-row class="mt-5" >
          <v-col cols="9">
            <v-subheader :class="['text-h5']">{{course.course_name}}</v-subheader>
          </v-col>
        </v-row>
        
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  props: {
    course_id: Number
  },
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.user_info = response.data
          self.is_creater = response.data.create
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
  methods:{
    move_to_course_info(){
      this.$router.push({name:'CourseInfo', params:{"course_id":this.course_id}})
    },
    move_to_course_taking(){
      this.$router.push({name:'CourseTaking',params:{"course_id":this.course_id}})
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
