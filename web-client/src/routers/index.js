import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AboutPage from '../views/AboutPage.vue'
import MonitorPage from '../views/MonitorPage.vue'
import ContactPage from '../views/ContactPage.vue'
import FAQ from '../views/FaqPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/', name: 'About', component: AboutPage },
  { path: '/', name: 'Monitor', component: MonitorPage },
  { path: '/', name: 'Contact', component: ContactPage },
  { path: '/faq', name: 'FAQ', component: FAQ }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
