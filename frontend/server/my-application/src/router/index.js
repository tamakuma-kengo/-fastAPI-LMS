import Vue from "vue";
import VueRouter from "vue-router";

import Top from "../components/pages/Top.vue";
import Login from "../components/pages/Login.vue";
import Signup from "../components/pages/Signup.vue";

import StudentHome from "../components/pages/students/StudentHome.vue";
import Course from "../components/pages/students/Course.vue";
import Flow from "../components/pages/students/Flow.vue";
import FlowSession from "../components/pages/students/FlowSession.vue";
import FlowCompletion from "../components/pages/students/FlowCompletion.vue";

import TeacherHome from "../components/pages/teachers/TeacherHome.vue";
import RegisterCourse from "../components/pages/teachers/RegisterCourse.vue";
import CourseInfo from "../components/pages/teachers/CourseInfo.vue";
import CourseTaking from "../components/pages/teachers/CourseTaking.vue";
import CoursePreview from "../components/pages/teachers/CoursePreview.vue";
import CourseEdit from "../components/pages/teachers/CourseEdit.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Root",
    redirect: function () {
      return "/Home";
    },
  },
  {
    path: "/Top",
    name: "Top",
    component: Top,
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
  // 生徒画面
  {
    path: "/Home",
    name: "StudentHome",
    component: StudentHome,
  },
  {
    path: "/Course/:course_id",
    name: "Course",
    component: Course,
    props: true,
  },
  {
    path: "/Course/:course_id/flow/:flow_id",
    name: "Flow",
    component: Flow,
    props: true,
  },
  {
    path: "/FlowSession/:flow_session_id/:page_num",
    name: "FlowSession",
    component: FlowSession,
    props: (route) => ({
      flow_session_id: Number(route.params.flow_session_id),
      page_num: Number(route.params.page_num),
    }),
  },
  {
    path: "/FlowSession/:flow_session_id/CompletionPage",
    name: "FlowCompletion",
    component: FlowCompletion,
    props: (route) => ({
      flow_session_id: Number(route.params.flow_session_id),
    }),
  },
  // Teacher画面
  {
    path: "/t/Home",
    name: "TeacherHome",
    component: TeacherHome,
  },
  {
    path: "/t/RegisterCourse",
    name: "RegisterCourse",
    component: RegisterCourse,
  },
  {
    path: "/t/CourseInfo/:course_id",
    name: "CourseInfo",
    component: CourseInfo,
    props: true,
  },
  {
    path: "/t/CourseTaking/:course_id",
    name: "CourseTaking",
    component: CourseTaking,
    props: true,
  },
  {
    path: "/t/CoursePreview/:course_id",
    name: "CoursePreview",
    component: CoursePreview,
    props: true,
  },
  {
    path: "/t/CourseEdit/:course_id",
    name: "CourseEdit",
    component: CourseEdit,
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
