<template>
    <v-container class="grey lighten-5">
        <v-row align="center" justify="space-around" >
            <v-btn depressed color="primary" @click="go_login_page()">
                Login
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around">
            <v-btn depressed color="primary" @click="go_signup_page()">
                Sign up
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around">
            <v-btn depressed color="primary" @click="set_cookie()">
                Sign up
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around">
            <v-btn depressed color="primary" @click="get_cookie()">
                Sign up
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
export default {
  name: "Top",
  data(){

  },
  methods:{
    go_login_page(){
      this.$router.push({name:'Login'})
    },
    go_signup_page(){
      this.$router.push({name:'Signup'})
    },
    set_cookie(){
      axios.get("http://127.0.0.1:8000/set_cookie",{withCredentials: true})
      .then(
        function(responce){
          console.log(responce)
        }
      )
    },
    get_cookie(){
      axios.get('http://127.0.0.1:8000/get_cookie',{withCredentials: true})
      .then(
        function(responce){
          console.log(responce)
        }
      )
    }
  }
};
</script>
