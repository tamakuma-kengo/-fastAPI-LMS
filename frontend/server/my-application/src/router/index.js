import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../components/pages/Home.vue";
import Top from "../components/pages/Top.vue";
import Login from "../components/pages/Login.vue";
import Signup from "../components/pages/Signup.vue";
import Home from "../components/pages/Home.vue";
import RegisterCourse from "../components/pages/RegisterCourse.vue";
import Uploads from "../components/pages/Uploads.vue";
import Courses from "../components/pages/Courses.vue";
import Course from "../components/pages/Course.vue";
import Flow from "../components/pages/Flow.vue";
import FlowSession from "../components/pages/FlowSession.vue";

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
    path: "/Courses",
    name: "Courses",
    component: Courses,
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
  },
  {
    path: "/Course/:course_id/flow/:flow_id",
    name: "Flow",
    component: Flow,
    props: true
  },
  {
    path: "/FlowSession/:flow_session_id/:page_num",
    name: "FlowSession",
    component: FlowSession,
    props: (route) => ({flow_session_id: Number(route.params.flow_session_id), page_num: Number(route.params.page_num)})
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
