<template>
    <v-container v-if="isCreater">
      <v-responsive :max-width="800" class="mx-auto">
        <v-container class="mt-8">
          <v-row justify="end">
            <v-btn text color="red" @click="logout()" value="POST">ログアウト</v-btn>
          </v-row>
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
                <v-col>
                  <v-text-field :rules="startDateRules" label="開始日 ex. 2022-02-04" v-model="startDate" background-color="white" filled error-count="10">
                    <template v-slot:append-outer>
                      <v-menu offset-y :close-on-content-click="false">
                        <template v-slot:activator="{on}">
                          <v-btn icon color="primary" dark elevation="0" v-on="on">
                            <v-icon>mdi-calendar</v-icon>
                          </v-btn>
                        </template>
                        <v-date-picker v-model="startDate"/>
                      </v-menu>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col>
                  <v-text-field :rules="startTimeRules" label="開始時間 ex. 13:30:00" v-model="startTime" background-color="white" filled error-count="10">
                    <template v-slot:append-outer>
                      <v-menu offset-y :close-on-content-click="false">
                        <template v-slot:activator="{on}">
                          <v-btn icon color="primary" dark elevation="0" v-on="on">
                            <v-icon>mdi-clock</v-icon>
                          </v-btn>
                        </template>
                        <v-time-picker v-model="startTime" format="24hr" use-seconds/>
                      </v-menu>
                    </template>
                  </v-text-field>
                </v-col>
                  <!-- <v-text-field :rules="startTimeRules" label="start time   ex. 23:30" v-model="startTime" background-color="white" filled></v-text-field> -->
              </v-row>
              <v-row align="center" justify="space-around" >
                <v-col>
                  <v-text-field :rules="endDateRules" label="終了日 ex. 2022-02-04" v-model="endDate" background-color="white" filled error-count="10">
                    <template v-slot:append-outer>
                      <v-menu offset-y :close-on-content-click="false">
                        <template v-slot:activator="{on}">
                          <v-btn icon color="primary" dark elevation="0" v-on="on">
                            <v-icon>mdi-calendar</v-icon>
                          </v-btn>
                        </template>
                        <v-date-picker v-model="endDate"/>
                      </v-menu>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col>
                  <v-text-field :rules="endTimeRules" label="終了時間 ex. 13:30:00" v-model="endTime" background-color="white" filled error-count="10">
                    <template v-slot:append-outer>
                      <v-menu offset-y :close-on-content-click="false">
                        <template v-slot:activator="{on}">
                          <v-btn icon color="primary" dark elevation="0" v-on="on">
                            <v-icon>mdi-clock</v-icon>
                          </v-btn>
                        </template>
                        <v-time-picker v-model="endTime" format="24hr" use-seconds/>
                      </v-menu>
                    </template>
                  </v-text-field>
                </v-col>
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
  name: "RegisterCoruse",
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
    startDateRules:[
      v => !!v || '開始日は必須です.',
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 2022-02-04'
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
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
        const pattern = /\d{4}-\d{2}-\d{2}/
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
        const pattern = /\d{4}-\d{2}-\d{2}/
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
    ],
    startTimeRules:[
      v => !!v || '開始時間は必須です.',
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 13:30:30'
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[0] > 23 || time_splited[0] < 0)
            return "時は0~23の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[1] > 59 || time_splited[1] < 0)
            return "分は0~59の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[2] > 59 || time_splited[2] < 0)
            return "秒は0~59の間で入力してください. " 
        }
        return true
      },
    ],
    endDateRules:[
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 2022-02-04 '
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
        if(pattern.test(v)){
          const date_splited = v.split("-")
          if (date_splited[0] > 2100 || date_splited[0] < 2000)
            return "年は2000~2100の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
        if(pattern.test(v)){
          const date_splited = v.split("-")
          if (date_splited[1] > 12 || date_splited[1] < 1)
            return "月は1~12の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{4}-\d{2}-\d{2}/
        if(pattern.test(v)){
          const date_splited = v.split("-")
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
    ],
    endTimeRules:[
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 13:30:30 '
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[0] > 23 || time_splited[0] < 0)
            return "時は0~23の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[1] > 59 || time_splited[1] < 0)
            return "分は0~59の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
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
    startDate: "",
    startTime: "",
    endDateTime: "",
    endDate: "",
    endTime: "",
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
    move_to_course_info(course_id){
      this.$router.push({name:'CourseInfo', params: {course_id: course_id, new_create: true}})
    },
    register_course(){
      this.startDateTime = this.startDate + " " + this.startTime
      this.endDateTime = this.endDate + " " + this.endTime
      const is_validation_success = this.validate_form()
      if(is_validation_success){
          const params = {"course_name":this.courseName,"start_date_time": this.startDateTime.replace(/\s/,"T"),"end_date_time":this.endDateTime.replace(/\s/,"T"),"course_files": this.files}
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
