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
        </v-col >  
        <v-col cols="2">
          <v-btn depressed block color="transparent"  class="mb-2">
            編集
          </v-btn>
          <v-divider class="red"></v-divider>
        </v-col>  
        </v-row>
        <v-divider class="mt-0"></v-divider>
        <v-row class="mt-5" >
          <v-responsive :max-width="1000" class="mx-auto">
            <v-container>
              <v-row>
                <v-col>
                  <v-subheader :class="['text-h5']">コース情報の変更</v-subheader>
                </v-col>
              </v-row>
              <v-row>
                <v-col class="pl-0 pb-0">
                  <v-subheader :class="['subtitle-1']">コース名</v-subheader>
                </v-col>
              </v-row>
              <v-row class="mt-0">
                <v-col cols="5">
                  <v-text-field v-model="course_name"  outlined dense></v-text-field>
                </v-col>
                <v-col cols="1">
                  <v-btn @click="update_course_name()" >更新</v-btn>
                </v-col>
              </v-row>
              <v-row class="mt-0">
                <v-col cols="5" class="pl-0 pb-0">
                  <v-subheader :class="['subtitle-1']">開始日時</v-subheader>
                </v-col>
                <v-col cols="5" class="pl-0 pb-0">
                  <v-subheader :class="['subtitle-1']">終了日時</v-subheader>
                </v-col>
              </v-row>
              <v-row class="mt-0">
                <v-col cols="5">
                  <v-text-field v-model="start_date_time"  outlined dense></v-text-field>
                </v-col>
                <v-col cols="5">
                  <v-text-field v-model="end_date_time"  outlined dense></v-text-field>
                </v-col>
                <v-col cols="1">
                  <v-btn @click="update_date_time()">更新</v-btn>
                </v-col>
              </v-row>
              
            </v-container>
          </v-responsive>
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
    user_info : {},
    is_create : false,
    course: {},
    course_name: "",
    start_date_time: "",
    end_date_time: "",
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
    get_course_info(){
      let self = this
      axios.get(`http://localhost:8000/get_course_info/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.course = response.data
          self.course_name = self.course.course_name
          self.start_date_time = self.course.start_date_time
          self.end_date_time = self.course.end_date_time
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
    update_course_name(){
      const params = {"course_id":this.course_id, "course_name": this.course_name}
      console.log(JSON.stringify(params));
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      let self = this
      axios.post('http://localhost:8000/update_course_name', params, config)
      .then(function(response){
        console.log(response.data)
          self.get_course_info()
      })
    },
    update_date_time(){
      const params = {"course_id":this.course_id, "start_date_time": this.start_date_time, "end_date_time": this.end_date_time}
      console.log(JSON.stringify(params));
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      let self = this
      axios.post('http://localhost:8000/update_date_time', params, config)
      .then(function(response){
        console.log(response.data)
          self.get_course_info()
      })
    }
  },
};
</script>
