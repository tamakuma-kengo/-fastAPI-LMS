<template>
  <v-responsive :min-height="50" >
    <v-container class="pa-0">
      <div :class="`rounded-lg`" class="blue lighten-4 pa-1" >
        <v-row no-gutters>
            <v-col cols="1">
              <v-container fill-height>
                <v-row no-gutters>
                  <v-btn @click="go_flow_top_page()" block class="pa-1">
                    Home
                  </v-btn>
                </v-row>
              </v-container>
            </v-col>
            <v-col cols="10" >
              <v-container class="pa-2" fill-height>
                <v-row no-gutters>
                  <v-col cols="1" class="pa-1" v-for="page_i in this.num_of_pages" :key=page_i>
                    <v-btn block class="pa-1" v-if="page_i==page_num" disabled="true" color="red">
                      {{page_i}}
                    </v-btn>
                    <v-btn block class="pa-1" @click="go_any_page(page_i)" v-if="page_i!=page_num">
                      {{page_i}}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-col>
            <v-col cols="1">
              <v-container fill-height>
                <v-row no-gutters>
                  <v-btn @click="finish_flow_session()" block class="pa-1">
                    終了
                  </v-btn>
                </v-row>
              </v-container>
            </v-col>
        </v-row>
      </div>
    </v-container>
  </v-responsive>
</template>

<script>
import axios from 'axios';

export default {
  name: "FlowSessionLocationBar",
  props: {
      flow_session_id: Number,
      page_num: Number,
      num_of_pages: Number
    },
  created: function() {
  },
  data: () => ({
  }),
  methods:{
     go_any_page(page_num){
       this.$router.push({name:'FlowSession', params: {flow_session_id: this.flow_session_id, page_num: page_num}})
     },
     go_flow_top_page(){
      let self = this
      axios.get(`http://localhost:8000/get_ids_by_flow_session_id/${self.flow_session_id}`, {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        let flow_id = response.data.flow_id
        self.$router.push({name:'Flow', params: {flow_id:flow_id}})
      }).catch(function(error){
        console.log(error.response)
      })
    },
    finish_flow_session(){
      const params = {"flow_session_id": this.flow_session_id}
      const config = {headers: {'Content-Type': 'application/json'},withCredentials: true};
      let self = this
      axios.post(`http://localhost:8000/finish_flow_session`, params, config)
      .then(function(response){
        console.log(response.data)
        self.go_flow_completion_page()
      }).catch(
        function(error){
          console.log(error)
        }
      )
    },
    go_flow_completion_page(){
      this.$router.push({name:'FlowCompletion', params: {flow_session_id: this.flow_session_id}})
    }
  },
};
</script>
