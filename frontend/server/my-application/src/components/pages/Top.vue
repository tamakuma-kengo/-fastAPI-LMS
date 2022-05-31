<template>
    <v-container class="grey lighten-5">
        <v-row align="center" justify="space-around" >
            <v-btn depressed color="primary" @click="go_login_page()">
                ログイン
            </v-btn>
        </v-row>
        <v-row align="center" justify="space-around">
            <v-btn depressed color="primary" @click="go_signup_page()">
                新しくアカウントを作成
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
export default {
  name: "Top",
  methods:{
    go_login_page(){
      this.$router.push({name:'Login'})
    },
    go_signup_page(){
      this.$router.push({name:'Signup'})
    },
  }
};
</script>
