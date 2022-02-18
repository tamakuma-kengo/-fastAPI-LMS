<template>
    <v-container >
      <v-subheader :class="['text-h5']">{{this.page.title}}</v-subheader>
      <FlowSessionLocationBar></FlowSessionLocationBar>
      <v-responsive :min-height="600">
        <v-container fluid >
            <component :is="componentName" :page_content='page_content' :flow_session_id='flow_session_id' :page_num='page_num'></component>
        </v-container>
      </v-responsive>
      <v-container >
        <v-row>
          <v-col >
            <v-btn @click="go_previous_page()" v-if="this.page_num > 1"> 前のページ  </v-btn>
          </v-col>
          <v-col class="d-flex align-end flex-column">
            <v-btn @click="go_next_page()"> 次のページ </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
</template>

<script>
import axios from "axios";
import SimplePage from '../modules/SimplePage.vue'
import SingleTextQuestion from '../modules/SingleTextQuestion.vue'
import MultipleTextQuestion from '../modules/MultipleTextQuestion.vue'
import DescriptiveTextQuestion from '../modules/DescriptiveTextQuestion.vue'
import ChoiceQuestion from '../modules/ChoiceQuestion.vue'
import FlowSessionLocationBar from '../modules/FlowSessionLocationBar.vue'

export default {
  name: "Flow",
  props: {
    flow_session_id: Number,
    page_num: Number
  },
  components: {
    SimplePage,
    SingleTextQuestion,
    MultipleTextQuestion,
    DescriptiveTextQuestion,
    ChoiceQuestion,
    FlowSessionLocationBar
  },
  created: function() {
    this.update_data()
  },
  data: () => ({
    page: {"title":""},
    page_content: {},
    username : "",
    is_creater : false,
    html: "# aaaaa",
    componentName: ""
  }),
  beforeRouteUpdate (to, from, next) {
    this.update_data()
    next();
  },
  methods:{
    update_data(){
    let self = this
    axios.get("http://127.0.0.1:8000/home_profile", {withCredentials: true})
    .then(function(response){
      console.log(response.data)
      self.username = response.data.username
      self.is_creater = response.data.create
      axios.get(`http://127.0.0.1:8000/get_flowpage/${self.flow_session_id}/${self.page_num}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.page = response.data
          self.page_content = response.data.page_content
          self.componentName = response.data.page_type
        }).catch(function(error){
          console.log(error.response)
        })
    }).catch(function(error)  {
      if(error.response.status == 401){
        self.$router.push({name:'Signup'})
      }else{
        console.log(error.response)
      }
    })
    },
    go_previous_page(){
      this.$router.push({name:'FlowSession', params: {flow_session_id: this.flow_session_id, page_num: this.page_num-1}})
    },
    go_next_page(){
      this.$router.push({name:'FlowSession', params: {flow_session_id: this.flow_session_id, page_num: this.page_num+1}})
    }
  },
};
</script>
