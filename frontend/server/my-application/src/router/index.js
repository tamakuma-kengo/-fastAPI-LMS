import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../components/pages/Home.vue";
import Top from "../components/pages/Top.vue";
import Login from "../components/pages/Login.vue";
import Signup from "../components/pages/Signup.vue";
import Home from "../components/pages/Home.vue";
import RegisterCourse from "../components/pages/RegisterCourse.vue";
import Uploads from "../components/pages/Uploads.vue";
import Course from "../components/pages/Course.vue";



Vue.use(VueRouter);

const routes = [
  {
    path: "/Uploads",
    name: "Uploads",
    component: Uploads,
  },
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
    name: "Home",
    component: Home,
  },
  {
    path: "/Course/:course_id",
    name: "Course",
    component: Course,
    props: true
  },
  {
    path: "/RegisterCourse",
    name: "RegisterCourse",
    component: RegisterCourse,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
