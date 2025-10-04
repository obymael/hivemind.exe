import { createRouter, createWebHistory } from 'vue-router'
import MonitorPage from '../views/MonitorPage.vue'
import FAQ from '../views/FaqPage.vue'

const routes = [
  { path: '/', name: 'Monitor', component: MonitorPage },
  { path: '/faq', name: 'FAQ', component: FAQ }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
