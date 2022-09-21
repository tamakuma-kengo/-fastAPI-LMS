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
            <v-row v-if="is_add && is_file == false">
              <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap">
                {{this.add_username}}を追加しました.
              </div>
            </v-row>
            <v-row v-else-if="is_add && is_file">
              <div :class="`rounded-lg`" class="pa-6 mt-6 green lighten-5 text-no-wrap">
                csvファイルからまとめて追加しました.
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
            <v-row class="mt-5" >
              <v-col cols="12">
                <v-subheader :class="['text-h5']">ユーザーをまとめて登録する場合は、こちらからcsvファイルを選択してください。</v-subheader>
              </v-col>
            </v-row>
            <div :class="`rounded-lg`" class="pa-8 mt-6 blue lighten-5 text-no-wrap">
              <v-row align="center" justify="space-around" >
                <input id="csvfile" v-on:change="onFileChange" type="file">
                <v-btn depressed color="primary" @click="add_fileusers()" value="POST">
                    まとめて登録する
                </v-btn>
              </v-row>
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
          self.get_users()
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
    file: "",
    fileusers: [],
    is_file: false,
    users: [],
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
      get_users(){
        let self = this
        axios.get("http://localhost:8000/get_users", {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.users = response.data
          }).catch(
            function(error){
              console.log(error)
            }
          )
      },
      add_user(username,email,password,kind_id){
        const params = {"username": username, "email": email, "password": password, "kind_id": kind_id}
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
      },
      add_users(){
        let is_validation_success = this.validate_form(this.add_username,this.add_email,this.add_password,this.add_kind_name)
        if(is_validation_success){
          this.add_user(this.add_username,this.add_email,this.add_password,this.add_kind_id)
        }
      },
      add_fileusers(){
        if(this.file.length == 0){this.error_msgs.push("csvファイルが選択されていません．ファイルを登録した後に，ボタンを押してください．")}
        else{
          this.is_file = true;
          for(let fileuser of this.fileusers){
            let is_validation_success = this.validate_form(fileuser.username,fileuser.email,fileuser.password,fileuser.kind_name)
            if(is_validation_success){
              this.add_user(fileuser.username,fileuser.email,fileuser.password,this.add_kind_id)
            }
          }
        }
      },
      validate_form(username,email,password,kind_name){
        this.error_msgs = []
        if(this.is_file == false ){
          if(this.$refs.add_user_form.validate()){
            if(username.length == 0 || email.length == 0 || password.length == 0 || this.re_password.length == 0){
              this.error_msgs.push("入力されていない項目があります．登録したい情報を入力してください．")
            }
            if(password != this.re_password){
              this.error_msgs.push("再入力されたパスワードが違います．パスワードが合っているか確認してください．")
            }
            if(kind_name.length == 0){
              this.error_msgs.push("studentかteacherか選択されていません．登録したいユーザーに合わせて選択してください．")
            }
          }
        }
        else{
          if(username.length == 0){
            this.error_msgs.push("ユーザ名が入力されていない箇所があります．ファイルを修正してください．")
          }
          if(email.length == 0){
            this.error_msgs.push("メールアドレスが入力されていない箇所があります．ファイルを修正してください．")
          }
          if(password.length == 0){
            this.error_msgs.push("パスワードが入力されていない箇所があります．ファイルを修正してください．")
          }
          if(kind_name.length == 0){
            this.error_msgs.push("studentかteacherを入力していない箇所があります．ファイルを修正してください．")
          }
          if(this.users.some(e => e.email == email)){
            this.error_msgs.push("すでに登録されているユーザーが存在します．ファイルのユーザ名，メールアドレスと登録されているユーザーに重複がないか確認した上で，再度ファイルの登録をお願いします．")
          }
        }
        if(kind_name == "teacher"){
          this.add_kind_id = 1
        }
        else if(kind_name == "student"){
          this.add_kind_id = 2
        }
        return this.error_msgs.length == 0
      },
      onFileChange(fileObjects) {
        this.file = fileObjects.target.files[0];
        const csvreader = new FileReader();

        const loadFunction = () => {
          const lines = csvreader.result.split('\n');
          const data = lines.filter(function(s){return s !== '';});
          data.forEach(e =>{
            const readusers = e.split(',');
            if(readusers.length != 4){
              this.error_msgs.push("登録されたcsvファイルのデータが間違っています．修正して，再度登録をお願いします．");
              return;
            }
            const users = {
              username: readusers[0],
              email: readusers[1],
              password: readusers[2],
              kind_name: readusers[3].replace('\r','')
            };
            this.fileusers.push(users);
          });
        };
        console.log(this.fileusers);
        csvreader.onload = loadFunction;
        csvreader.readAsBinaryString(this.file);
      },
  },
};
</script>
