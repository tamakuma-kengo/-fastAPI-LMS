<template>
  <v-responsive :min-height="50" >
    <v-container class="pa-0">
      <div :class="`rounded-lg`" class="blue lighten-4 pa-1" >
        <v-row no-gutters>
            <v-col cols="1">
              <v-container fill-height>
                <v-row no-gutters>
                  <v-btn block class="pa-1">
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
                  <v-btn block class="pa-1">
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
     }
  },
};
</script>
