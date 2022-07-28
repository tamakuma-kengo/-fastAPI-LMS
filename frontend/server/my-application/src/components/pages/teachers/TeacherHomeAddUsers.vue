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
              <v-row justify="end">
                <v-btn text color="red" @click="logout()" value="POST">ログアウト</v-btn>
              </v-row>
            </v-container>
          </v-responsive>
        </v-row>
        <v-row>
          <v-container v-if="is_create" class="pa-0">
            <v-row>
            <v-col cols="2">
              <v-btn @click="move_to_select_courses()" depressed block color="transparent"  class="mb-2"> 
                コース一覧
              </v-btn>
            </v-col>  
            <v-col cols="2">
              <v-btn @click="move_to_add_users()" depressed block color="transparent"  class="mb-2">
                ユーザーの登録
              </v-btn>
              <v-divider class="red"></v-divider>
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
                <v-subheader :class="['text-h5']">新しいユーザーの登録</v-subheader>
              </v-col>
            </v-row>
            <v-row v-if="is_add">
              <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap">
                {{this.add_username}}を追加しました.
              </div>
            </v-row>
            <div :class="`rounded-lg`" class="pa-6 mt-6 red lighten-5 text-no-wrap" v-if="error_msgs.length>0">
              <v-row>
                ○ エラー
              </v-row>
              <v-row v-for="(msg,i) in error_msgs" :key="i" class="pl-3">
                {{"・ "+msg}}
              </v-row>
            </div>
            <div :class="`rounded-lg`" class="pa-8 mt-6 grey lighten-3 text-no-wrap">
            <v-form ref="add_user_form">
              <v-row align="center" justify="space-around" >
                <v-text-field label="ユーザー名" v-model="add_username" background-color="white" filled ></v-text-field>
              </v-row>
              <v-row align="center" justify="space-around" >
                <v-text-field label="メールアドレス" v-model="add_email" background-color="white" filled ></v-text-field>
              </v-row>
              <v-row align="center" justify="space-around" >
                <v-text-field label="パスワード" v-model="add_password" background-color="white" filled ></v-text-field>
              </v-row>
              <v-row align="center" justify="space-around" >
                <v-text-field label="パスワードの再入力" v-model="re_password" background-color="white" filled ></v-text-field>
              </v-row>
              <v-row align="center" justify="space-around" >
                <v-select :items="kind_names" label="生徒・教師の選択" v-model="add_kind_name" background-color="white" outlined></v-select>
              </v-row>
              <v-row align="center" justify="space-around" class="mt-8" >
                <v-btn depressed color="primary" @click="add_users()" value="POST">
                    ユーザーの登録
                </v-btn>
              </v-row>
            </v-form>
            </div>
          </v-container>
        </v-row>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "AddUsers",
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
    add_username: "",
    add_email: "",
    add_password: "",
    re_password: "",
    kind_names: ["student","teacher"],
    add_kind_name: "",
    add_kind_id: 0,
    error_msgs: [],
    is_add : false,
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
      move_to_select_courses(){
        this.$router.push({name:'TeacherHome'})
      },
      move_to_add_users(){
        this.$router.push({name:'AddUsers'})
      },
      add_users(){
        const is_validation_success = this.validate_form()
        if(is_validation_success){
          const params = {"username":this.add_username, "email": this.add_email, "password":this.add_password, "kind_id": this.add_kind_id}
          console.log(JSON.stringify(params));
          const config = {
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials: true
          };
          let self = this
          axios.post('http://localhost:8000/add_users', params, config)
          .then(function(response){
            console.log(response.data)
            if(response.data.success){
              self.is_add = true
            }else{
              self.error_msgs = [response.data.error_msg]
            }
          })
        }
      },
      validate_form(){
        this.error_msgs = []
        if(this.$refs.add_user_form.validate()){
          if(this.add_username.length == 0 || this.add_email.length == 0 || this.add_password.length == 0 || this.re_password.length == 0){
            this.error_msgs.push("入力されていない項目があります．登録したい情報を入力してください．")
          }
          if(this.add_password != this.re_password){
            this.error_msgs.push("再入力されたパスワードが違います．パスワードが合っているか確認してください．")
          }
          if(this.add_kind_name.length == 0){
            this.error_msgs.push("studentかteacherか選択されていません．登録したいユーザーに合わせて選択してください．")
          }
        }
        if(this.add_kind_name == "teacher"){
          this.add_kind_id = 1
        }
        else if(this.add_kind_name == "student"){
          this.add_kind_id = 2
        }
        return this.error_msgs.length == 0
      },
  },
};
</script>
