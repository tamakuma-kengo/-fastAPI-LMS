<template>
    <v-container v-if="isCreater">
        <h2>Register New Course</h2>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="titleRules" label="course name" v-model="courseName"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="startDateRules" label="start date   ex. 2020-10-04" v-model="startDate"></v-text-field>
            <v-text-field :rules="startTimeRules" label="start time   ex. 23:30" v-model="startTime"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="endDateRules" label="end date" v-model="endDate"></v-text-field>
            <v-text-field :rules="startTimeRules" label="end time" v-model="startTime"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
          <input id="image" v-on:change="onFileChange" type="file" webkitdirectory>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-btn depressed color="primary" @click="register_course()" value="POST">
                Register
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around" >
            {{this.error_msgs}}
        </v-row>
    </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: "Home",
  created: function() {
    let self = this
    axios.get("http://127.0.0.1:8000/users/creater", {withCredentials: true})
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
      v => !!v || 'title is required',
    ],
    startDateRules:[
      v => !!v || 'start date is required',
    ],
    startTimeRules:[
      v => !!v || 'start time is required',
    ],
    endDateRules:[
      v => !!v || 'end date is required',
    ],
    endTimeRules:[
      v => !!v || 'end time is required',
    ],
    files: [],
    error_msgs: "",
    test_text: "",
    startDate: "",
    startTime: "",
    endDate: "",
    endTime: "",
    courseName: "",
  }),
  methods:{
      register_course(){
        const params = {"course_name":"サンプルコース1","start_date_time": "2022-2-10T00:00:00","end_date_time":"2022-05-10T23:59:59","course_files": this.files}
        console.log(JSON.stringify(params));
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        let self = this
        axios.post('/api/register_course', params, config)
        .then(function(response){
          console.log(response.data)
          if (response.data.success){
            self.$router.push({name:'Course', params: {course_id: response.data.registered_course.id}})
          }else{
            self.error_msgs = response.data.error_msg
          }
        })
      },
      onFileChange(fileObjects) {
        const files = fileObjects.target.files;
        const fileForUpload = [];
        for(let file of files){
          let filePath = file.webkitRelativePath;
          let fileReader = new FileReader();
          fileReader.onload = event => {
            let text = event.target.result;
            console.log(text)
            fileForUpload.push({file_path:filePath,file_text:text})
            console.log(fileForUpload[0]["file_text"])
          }
          fileReader.readAsText(file);
        }
        this.files = fileForUpload;
    },
  },
};
</script>
