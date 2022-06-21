<template>
    <v-container>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="email_rules" label="email" v-model="email"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-text-field 
            :append-icon="pswd ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="password_rules" 
            :type="pswd ? 'text' : 'password'"
            label="password" 
            class="input-group--focused"
            @click:append="pswd = !pswd"
            v-model="password"
            ></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-btn depressed color="primary" @click="login()" value="POST">
                ログイン
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
export default {
  
  name: "Login",
  data: () => ({
      pswd: false,
      email: "neo@neo.com",
      password: "neoneo",
      email_rules: [
        value => !!value || 'Required.',
      ],
      password_rules: [
        value => !!value || 'Required.',
      ]
    }),
  methods:{
      login: function(){
        console.log(this.email,this.password)
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        const params = {email: this.email,password: this.password}
        let self = this
        axios.post("http://localhost:8000/token", params, config)
        .then(function(response){
          console.log(response.data)
          axios.get("http://localhost:8000/home_profile", {withCredentials: true})
          .then(function(response){
              if(response.data.create){
                self.go_teacher_home()
              }else{
                self.go_students_home()
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
          )}
        ).catch(
          function(error){
            console.log(error)
          }
        )
      },
      go_signup_page: function(){
          this.$router.push({name:'Signup'})
      },
      go_students_home: function(){
          this.$router.push({name:'StudentHome'})
      },
      go_teacher_home: function(){
          this.$router.push({name:'TeacherHome'})
      },

  },
};
</script>
