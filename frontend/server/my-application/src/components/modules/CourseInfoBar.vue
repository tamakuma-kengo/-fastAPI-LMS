<template>
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
        <v-divider class="red" v-if="this.select_id == 1"></v-divider>
    </v-col>
    <v-col cols="2">
        <v-btn @click="move_to_course_taking()" depressed block color="transparent"  class="mb-2">
        履修者
        </v-btn>
        <v-divider class="red" v-if="this.select_id == 2"></v-divider>
    </v-col >  
    <v-col cols="2">
        <v-btn @click="move_to_course_preview()" depressed block color="transparent"  class="mb-2">
        プレビュー
        </v-btn>
        <v-divider class="red" v-if="this.select_id == 3"></v-divider>
    </v-col >  
    <v-col cols="2">
        <v-btn @click="move_to_course_edit()" depressed block color="transparent"  class="mb-2">
        編集
        </v-btn>
        <v-divider class="red" v-if="this.select_id == 4"></v-divider>
    </v-col>
    </v-row>
    <v-divider class="mt-0"></v-divider>
    <br>
  </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: "Home",
  props: {
    select_id: Number,
    course_id: Number,
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
    course_info_syllabus: {},
  }),
  methods:{
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
    },
  },
};
</script>
