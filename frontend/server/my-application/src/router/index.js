import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../components/pages/Home.vue";
import Top from "../components/pages/Top.vue";
import Login from "../components/pages/Login.vue";
import Signup from "../components/pages/Signup.vue";


Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Root",
  },
  {
    path: "/Top",
    name: "Top",
    component: Top
  },
  {
    path: "/Login",
    name: "Login",
    component: Login,
  },
  {
    path: "/Signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/Home",
    name: "Home"
    // component: Home,
  },
  {
    path: "/Course",
    name: "Course"
    // component: Course
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
