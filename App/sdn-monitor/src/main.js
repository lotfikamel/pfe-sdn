import Vue from 'vue'
import App from './App.vue'
import router from './Router/index'
import store from './Store/index'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
