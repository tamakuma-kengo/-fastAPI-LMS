<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <CourseInfoBarVue :select_id="2" :course_id="this.course_id"></CourseInfoBarVue>
        <v-row class="mt-5" >
          <v-responsive :max-width="1000" class="mx-auto">
            <v-container>
              <v-row>
                <v-col>
                  <v-subheader :class="['text-h5']">履修中のユーザ</v-subheader>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-data-table
                    :headers="headers"
                    :items="taking_students"
                    :items-per-page="5"
                    :search="search"
                    
                  ></v-data-table>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-subheader :class="['text-h5']">履修者の追加</v-subheader>
                </v-col>
              </v-row>
              <v-row >
                <v-col cols="5">
                  <v-text-field v-model="add_email" label="Emailアドレスを入力" outlined dense></v-text-field>
                </v-col>
                <v-col cols="1">
                  <v-btn @click="add_taking_students()" color="primary">追加</v-btn>
                </v-col>
              </v-row>
              <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap" v-if="is_taking">
                {{this.add_username}}が追加されました。
              </div>
            </v-container>
          </v-responsive>
        </v-row>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
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
    this.get_home_profile()
  },
  data: () => ({
    
    headers: [
      {text: "ユーザ名", value:"username"},
      {text: "Email", value:"email"},
      {text: "アクティブ", value:"is_active"},
      {text: "種別", value:"kind_name"}
    ],
    user_info : {},
    is_create : false,
    course: {},
    taking_students: [],
    add_email: "",
    add_user_error: "",
    is_taking: false,
    add_username: "",
  }),
  methods:{
    get_home_profile(){
      let self = this
      axios.get("http://localhost:8000/home_profile", {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.user_info = response.data
        self.is_creater = response.data.create
        if(self.is_creater){
          self.get_course_info()
          self.get_taking_students()
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
    get_taking_students(){
      let self = this
      axios.get(`http://localhost:8000/get_taking_students/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.taking_students = response.data
          for(let user of self.taking_students){
            if(user.email == self.add_email){
              self.add_username = user.username
            }
          }
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
    add_taking_students(){
      const params = {"course_id":this.course_id, "email": this.add_email}
      console.log(JSON.stringify(params));
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      let self = this
      axios.post('http://localhost:8000/register_taking_student', params, config)
      .then(function(response){
        console.log(response.data)
        self.get_taking_students()
        self.is_taking = true
      })
    }
  },
};
</script>
