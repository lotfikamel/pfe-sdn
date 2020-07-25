import Vue from 'vue'
import VueRouter from 'vue-router'
import FlowPage from '@/Pages/FlowPage/FlowPage.vue'
import TopologyPage from '@/Pages/TopologyPage/TopologyPage.vue'
import BwPage from '@/Pages/BwPage/BwPage.vue'

Vue.use(VueRouter)

const routes = [
   {
      path: '/',
      name: 'FlowPage',
      component: FlowPage
   },
   {
      path: '/topology',
      name: 'TopologyPage',
      component: TopologyPage
   },
   {
      path : '/bw',
      name: 'Bw',
      component : BwPage
   }
]

const router = new VueRouter({

   mode: 'history',
   base: process.env.BASE_URL,
   routes
})

export default router
