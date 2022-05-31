<template>
    <v-container class="grey lighten-5">
        <v-row align="center" justify="space-around" @click="go_login_page()">
            <v-btn depressed color="primary" href="/Login">
                ログイン
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around">
            <v-btn depressed color="primary" href="/Signup">
                新しくアカウントを作成
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>

export default {
  name: "Signup",
  data(){

  },
  methods:{
    //   go_login_page(){
    //         this.$router.push({name:'Login'})
    //   },
    //   go_signup_page(){
    //       this.$router.push({name:'Signup'})
    //   }
  }
};
</script>
