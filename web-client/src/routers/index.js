import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import FAQ from '../views/FaqPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/faq', name: 'FAQ', component: FAQ }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
