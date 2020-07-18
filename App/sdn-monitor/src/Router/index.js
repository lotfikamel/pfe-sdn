import Vue from 'vue'
import VueRouter from 'vue-router'
import FlowPage from '@/Pages/FlowPage/FlowPage.vue'

Vue.use(VueRouter)

const routes = [
   {
      path: '/',
      name: 'FlowPage',
      component: FlowPage
   }
]

const router = new VueRouter({

   mode: 'history',
   base: process.env.BASE_URL,
   routes
})

export default router
