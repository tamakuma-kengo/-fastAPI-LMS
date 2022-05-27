<template>
    <v-container v-if="isCreater">
      <v-responsive :max-width="800" class="mx-auto">
        <v-row justify="end">
          <v-btn text color="grey" @click="logout()" value="POST">logout</v-btn>
        </v-row>
        <v-container class="mt-8">
          <h2>新規コースの登録</h2>
          <div :class="`rounded-lg`" class="pa-6 mt-6 red lighten-5 text-no-wrap" v-if="error_msgs.length>0">
            <v-row>
              ○ エラー
            </v-row>
            <v-row v-for="(msg,i) in error_msgs" :key="i" class="pl-3">
              {{"・ "+msg}}
            </v-row>
          </div>
          <div :class="`rounded-lg`" class="pa-8 mt-6 grey lighten-3 text-no-wrap">
            <v-form ref="register_form">
              <v-row align="center" justify="space-around" >
                <v-text-field :rules="titleRules" label="コース名" v-model="courseName" background-color="white" filled ></v-text-field>
              </v-row>
              <v-row align="center" justify="space-around" >
                  <v-text-field :rules="startDateTimeRules" label="開始日時 ex. 2022-02-04 13:30:00" v-model="startDateTime" background-color="white" filled error-count="10"></v-text-field>
                  <!-- <v-text-field :rules="startTimeRules" label="start time   ex. 23:30" v-model="startTime" background-color="white" filled></v-text-field> -->
              </v-row>
              <v-row align="center" justify="space-around" >
                  <v-text-field :rules="endDateTimeRules" label="終了日時 ex. 2023-10-31 23:59:59" v-model="endDateTime" background-color="white" filled error-count="10"></v-text-field>
                  <!-- <v-text-field :rules="startTimeRules" label="end time" v-model="startTime" background-color="white" filled></v-text-field> -->
              </v-row>
              <v-row align="center" justify="space-around" >
                <input id="image" v-on:change="onFileChange" type="file" webkitdirectory >
              </v-row>
              <v-row align="center" justify="space-around" class="mt-8" >
                <v-btn depressed color="primary" @click="register_course()" value="POST">
                    コースを登録
                </v-btn>
              </v-row>
            </v-form>
          </div>
        </v-container>
      </v-responsive>
    </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: "Home",
  created: function() {
    let self = this
    axios.get("http://localhost:8000/users/creater", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.username = response.data.username
          self.isCreater = response.data.create
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
    isCreater: false,
    titleRules:[
      v => !!v || 'コース名は必須です.',
    ],
    startDateTimeRules:[
      v => !!v || '開始日時は必須です.',
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 2022-02-04 13:30:30 '
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[0] > 2100 || date_splited[0] < 2000)
            return "年は2000~2100の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[1] > 12 || date_splited[1] < 1)
            return "月は1~12の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[1] == 2){
            if (date_splited[0]%400==0){
              if (date_splited[2] > 29 || date_splited[2] < 0)
                return "日の値が不正です. " 
            }else if(date_splited[0]%100==0){
              if (date_splited[2] > 28 || date_splited[2] < 1)
                return "日の値が不正です. "
            }else if(date_splited[0]%4==0){
              if (date_splited[2] > 29 || date_splited[2] < 1)
                return "日の値が不正です. "
            }else{
              if (date_splited[2] > 28 || date_splited[2] < 1)
                return "日の値が不正です. "
            }
          }
          else if (["1","3","5","7","8","10","12"].includes(date_splited[1])){
            if (date_splited[2] > 31 || date_splited[2] < 1)
              return "日の値が不正です. " 
          }else{
            if (date_splited[2] > 30 || date_splited[2] < 1)
              return `日の値が不正です.` 
          }
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[0] > 23 || time_splited[0] < 0)
            return "時は0~23の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[1] > 59 || time_splited[1] < 0)
            return "分は0~59の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[2] > 59 || time_splited[2] < 0)
            return "秒は0~59の間で入力してください. " 
        }
        return true
      },
    ],
    endDateTimeRules:[
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 2022-02-04 13:30:30 '
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[0] > 2100 || date_splited[0] < 2000)
            return "年は2000~2100の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[1] > 12 || date_splited[1] < 1)
            return "月は1~12の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const date_splited = date_time_splited[0].split("-")
          if (date_splited[1] == 2){
            if (date_splited[0]%400==0){
              if (date_splited[2] > 29 || date_splited[2] < 0)
                return "日の値が不正です. " 
            }else if(date_splited[0]%100==0){
              if (date_splited[2] > 28 || date_splited[2] < 1)
                return "日の値が不正です. "
            }else if(date_splited[0]%4==0){
              if (date_splited[2] > 29 || date_splited[2] < 1)
                return "日の値が不正です. "
            }else{
              if (date_splited[2] > 28 || date_splited[2] < 1)
                return "日の値が不正です. "
            }
          }
          else if (["1","3","5","7","8","10","12"].includes(date_splited[1])){
            if (date_splited[2] > 31 || date_splited[2] < 1)
              return "日の値が不正です. " 
          }else{
            if (date_splited[2] > 30 || date_splited[2] < 1)
              return `日の値が不正です.` 
          }
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[0] > 23 || time_splited[0] < 0)
            return "時は0~23の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[1] > 59 || time_splited[1] < 0)
            return "分は0~59の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const date_time_splited = v.split(" ")
          const time_splited = date_time_splited[1].split(":")
          if (time_splited[2] > 59 || time_splited[2] < 0)
            return "秒は0~59の間で入力してください. " 
        }
        return true
      },
    ],
  
    files: [],
    error_msgs: [],
    courseName: "",
    startDateTime: "",
    endDateTime: "",
  }),
  methods:{
    logout: function(){
      let self = this
      axios.get("http://localhost:8000/home_profile", {withCredentials: true})
      .then(function(response){
        if(response.data.is_active){
          self.go_login_page()
        }
      }).catch(
        function(error){
          console.log(error)
          if(error.response.status == 401){
            self.$router.push({name:'Login'})
          }else{
            console.log(error.response)
          }
        }
      )
    },
    go_login_page: function(){
      this.$router.push({name:'Login'})
    },
    move_to_course_info(course_id){
      this.$router.push({name:'CourseInfo', params: {course_id: course_id}})
    },
    register_course(){
      const is_validation_success = this.validate_form()
      if(is_validation_success){
          const params = {"course_name":this.courseName,"start_date_time": "2022-2-10T00:00:00","end_date_time":"2022-05-10T23:59:59","course_files": this.files}
          console.log(JSON.stringify(params));
          const config = {
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials: true
          };
          let self = this
          axios.post('http://localhost:8000/register_course', params, config)
          .then(function(response){
            console.log(response.data)
            if (response.data.success){
              self.move_to_course_info(response.data.registered_course.id)
            }else{
              self.error_msgs = [response.data.error_msg]
            }
          })
      }
    },
    validate_form(){
      this.error_msgs = []
      if(this.$refs.register_form.validate()){
        if(this.endDateTime.length != 0){
          const start_date_time = new Date(this.startDateTime)
          const end_date_time = new Date(this.endDateTime)
          if(start_date_time >= end_date_time){
            this.error_msgs.push("終了日時には, 開始日時より未来の日付を入力してください.")
          }
        }
      }
      if(this.files.length == 0)
          this.error_msgs.push("登録するコースのフォルダを選択してください. ")
      return this.error_msgs.length == 0

    },
    onFileChange(fileObjects) {
      this.files = []
      const files = fileObjects.target.files;
      const fileForUpload = [];
      for(let file of files){
        let filePath = file.webkitRelativePath;
        let fileReader = new FileReader();
        console.log("file type: "+file.type)
        if(file.type.indexOf("image") != -1){
          fileReader.onload = function(e){
            let result = ""
            let int8_array = new Uint8Array(e.target.result);
            var i;
            var str;
            var num = int8_array.length;
            for(i=0;i<num;i++){
              if(int8_array[i] < 0x10){
                str = "0" + int8_array[i].toString(16);
              }else{
                str = int8_array[i].toString(16);
              }
              result += "\\x"+str
            }
            console.log(result)
            fileForUpload.push({file_path:filePath,file_text:result})
          }
          fileReader.readAsArrayBuffer(file)
        }else{
          fileReader.onload = function(e){
            console.log(e.target.result)
            fileForUpload.push({file_path:filePath,file_text:e.target.result})
          }
          fileReader.readAsText(file)
        }
      }
      this.files = fileForUpload;
    },
  },
};
</script>
