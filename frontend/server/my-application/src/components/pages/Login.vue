<template>
    <v-container>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="email_rules" label="email" v-model="email"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="password_rules" label="password" v-model="password"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-btn depressed color="primary" @click="login()" value="POST">
                Login
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
export default {
  
  name: "Login",
  data: () => ({
      email_rules: [
        value => !!value || 'Required.',
        // value => (value || '').length <= 20 || 'Max 20 characters',
        // value => {
        //   const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        //   return pattern.test(value) || 'Invalid e-mail.'
        // },
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
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        };
        const params = new URLSearchParams();
        params.append('username', this.email);    // 渡したいデータ分だけappendする
        params.append('password', this.password);
        axios
          .post("http://localhost:8000/token", params, config)
          .then(
            function(responce){
              console.log(responce)
            }
          )
      },
      go_signup_page: function(){
          this.$router.push({name:'Signup'})
      },
  },
};
</script>
