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
          <v-container v-if="is_create" class="pa-0">
            <v-row>
            <v-col cols="2">
              <v-btn depressed block color="transparent"  class="mb-2"> 
                コース一覧
              </v-btn>
              <v-divider class="red"></v-divider>
            </v-col>  
            <v-col cols="2">
              <v-btn depressed block color="transparent"  class="mb-2">
                かりおき
              </v-btn>
            </v-col >  
            <v-col cols="2">
              <v-btn depressed block color="transparent"  class="mb-2">
                かりおき
              </v-btn>
            </v-col>  
            </v-row>
            <v-divider class="mt-0"></v-divider>
            <v-row class="mt-5" >
              <v-col cols="9">
                <v-subheader :class="['text-h5']">作成したコース</v-subheader>
              </v-col>
              <v-col>
                <v-btn depressed color="primary" @click="add_course()" value="POST">
                  + 新しいコース
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="pa-2">
              <v-col cols="3" v-for="course in this.courses" :key="course.course_id">
                <v-card @click="move_to_course_info(course.course_id)">
                  <v-card-text>
                    <p class="text-h6 text--primary">
                      {{course.course_name}}
                    </p>
                    <div class="body-2">{{course.start_date_time}}</div>
                    <div class="body-2">{{course.end_date_time}}</div>
                  </v-card-text>
                </v-card>
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

export default {
  name: "TeacherHome",
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.user_info = response.data
          self.is_create = response.data.create
          if(self.is_create){
            self.get_created_courses()
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
    courses: {},
  }),
  methods:{
      add_course(){
        this.$router.push({name:'RegisterCourse'})
      },
      move_to_course_info(course_id){
        this.$router.push({name:'CourseInfo',params:{"course_id":course_id}})
      },
      get_created_courses(){
        let self = this
        axios.get(`http://localhost:8000/get_created_courses`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.courses = response.data
        }).catch(function(error)  {
          if(error.response.status == 401){
            self.$router.push({name:'Login'})
          }else{
            console.log(error.response)
          }
        }
      )
    }
  },
};
</script>
