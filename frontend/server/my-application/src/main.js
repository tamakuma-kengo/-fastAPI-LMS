import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueCookie from 'vue-cookie';
import VueUploadComponent from "vue-upload-component"

Vue.config.productionTip = false;

Vue.component('file-upload', VueUploadComponent)
new Vue({
  router,
  store,
  vuetify,
  VueCookie,
  render: (h) => h(App),
}).$mount("#app");
