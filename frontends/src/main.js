import Vue from 'vue'
import App from './App.vue'
// import router from './router'
// import store from './store'
import  {VueJsonp} from 'vue-jsonp'
import 'font-awesome/css/font-awesome.min.css'
import {Button} from 'vant'
import Meta from 'vue-meta'

Vue.config.productionTip = false
Vue.use(VueJsonp)
Vue.use(Button)
Vue.use(Meta)


new Vue({
  // router,
  // store,
  metaInfo: {
    title: 'Share your position',
    meta: [
      { charset: 'utf-8'},
      {name: 'viewport',content: 'width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no'}
    ]
  },
  render: h => h(App)
}).$mount('#app')
