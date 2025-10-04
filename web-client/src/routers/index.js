import { createRouter, createWebHistory } from 'vue-router'
import MonitorPage from '../views/MonitorPage.vue'
import FAQ from '../views/FaqPage.vue'
import VegetationIndexPage from '../views/VegetationIndexPage.vue'

const routes = [
  { path: '/', name: 'Monitor', component: MonitorPage },
  { path: '/faq', name: 'FAQ', component: FAQ },
  { path: '/vegetation-index', name: 'VegetationIndex', component: VegetationIndexPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
