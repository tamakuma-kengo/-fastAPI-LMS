<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap" v-if="new_create">
          コース登録が完了しました。履修者ページから、コースに参加する生徒を追加してください。
        </div>
        <CourseInfoBarVue :select_id="1" :course_id="this.course_id"></CourseInfoBarVue>
        <v-row>
          <v-col>
            <v-subheader :class="['text-h5']">科目情報</v-subheader>
          </v-col>
        </v-row>
        <v-simple-table>
          <thead>
            <tr>
              <th class="text-left">
                授業科目区分
              </th>
              <th class="text-left">
                科目名
              </th>
              <th class="text-left">
                単位
              </th>
              <th class="text-left">
                科目コード
              </th>
              <th class="text-left">
                開講時期
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ course_info_syllabus.subject_class }}</td>
              <td>{{ course_info_syllabus.subject_name }}</td>
              <td>{{ course_info_syllabus.subject_credit }}</td>
              <td>{{ course_info_syllabus.subject_code }}</td>
              <td>{{ course_info_syllabus.subject_period }}</td>
            </tr>
          </tbody>
        </v-simple-table>
        <v-divider class="mt-0"></v-divider>
      </v-container>
    </v-responsive>
  </v-container>
</template>
<style>
table thead tr th {
	color: #fff;
	background: #d0eafd;
}
</style>

<script>
import axios from "axios";
import CourseInfoBarVue from "../../modules/CourseInfoBar.vue";

export default {
  name: "Home",
  props: {
    course_id: Number,
    new_create: Boolean,
  },
  components: {
    CourseInfoBarVue,
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
          self.add_teachers()
          self.get_course_info_syllabus()
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
    add_teachers(){
    const params = {"course_id":this.course_id, "email":this.user_info.email}
    console.log(JSON.stringify(params));
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      axios.post('http://localhost:8000/register_taking_student', params, config)
      .then(function(response){
        console.log(response.data)
      })
    },
    get_course_info_syllabus(){
      let self = this
      axios.get(`http://localhost:8000/get_course_info_syllabus/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          for(const response_dict of response.data){
            self.course_info_syllabus = response_dict
          }
        }).catch(
          function(error){
            console.log(error)
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
