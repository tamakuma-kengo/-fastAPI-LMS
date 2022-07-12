<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <CourseInfoBarVue :select_id="3" :course_id="this.course_id"></CourseInfoBarVue>
        <v-row>
<<<<<<< HEAD
          <FlowVue :course_id="this.course_id" :flow_id="this.flow_id"></FlowVue>
=======
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
          <v-divider class="red"></v-divider>
        </v-col >  
        <v-col cols="2">
          <v-btn @click="move_to_course_edit()" depressed block color="transparent"  class="mb-2">
            編集
          </v-btn>
        </v-col>  
        </v-row>
        <v-divider class="mt-0"></v-divider>
        <br>
        <v-subheader :class="['text-h5']">{{flow.title}}</v-subheader>
        <v-row class="mt-5">
          <v-responsive >
            <v-container class="pa-0">
              <div :class="`rounded-lg`" class="grey lighten-3" v-if="this.flow_sessions.length > 0">
                <v-container class="pa-1">
                  <v-row no-gutters>
                    <v-col cols="1" class="text-center">
                      #
                    </v-col>
                    <v-col cols="3" class="text-center">
                      開始時刻
                    </v-col>
                    <v-col cols="3" class="text-center">
                      終了時刻
                    </v-col>
                    <v-col cols="2" class="text-center">
                      テスト回答済み
                    </v-col>
                    <v-col cols="2" class="text-center">
                      Grade
                    </v-col>
                    <v-col cols="1" class="text-center">
                      再スタート
                    </v-col>
                  </v-row>
                  <v-row v-for="(flow_session,i) in this.flow_sessions" :key="flow_session.id" class="pa-0 ma-0" no-gutters>
                    <v-col cols="1" class="text-center">
                      {{i+1}}
                    </v-col>
                    <v-col cols="3" class="text-center">
                      {{flow_session.start_date_time}}
                    </v-col>
                    <v-col cols="3" v-if="flow_session.finish_date_time" class="text-center">
                      {{flow_session.finish_date_time}}
                    </v-col>
                    <v-col cols="3" v-else class="text-center">
                      null
                    </v-col>
                    <v-col cols="2" class="text-center">
                      {{flow_session.is_finished}}
                    </v-col>
                    <v-col cols="2" class="text-center">
                      {{flow_session.flow_session_grade.toFixed(1)}}%
                    </v-col>
                    <v-col cols="1" class="text-center pa-1" >
                      <v-btn @click="restart_flow_session(flow_session.id)" small>
                        start
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </div>
            </v-container>
          </v-responsive>
          <v-container class="mt-6">
            <v-row>
              <div v-html="markdownToHtml(welcome_page_content)"></div>
            </v-row>
            <v-row class="mt-8">
              <v-btn depressed color="primary" @click="start_new_flow_session()">
                演習問題を開始
              </v-btn>
            </v-row>
            <v-row class="mt-8">
              <v-btn depressed color="primary" @click="go_to_course()">
                教科書ページに戻る
              </v-btn>
            </v-row>
          </v-container>
>>>>>>> 7c5367bb3f7e0cc43548588ccbd3dd9c49f8e537
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
