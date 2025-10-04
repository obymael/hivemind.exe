import { createRouter, createWebHistory } from 'vue-router'

// adjust paths to match your project
import HomePage from '../views/HomePage.vue'
import AboutPage from '../views/AboutPage.vue'
import MonitorPage from '../views/MonitorPage.vue'
import ContactPage from '../views/ContactPage.vue'
import FaqPage from '../views/FaqPage.vue'

const routes = [
  { path: '/',        component: HomePage,   meta: { headerVariant: 'home'  } },
  { path: '/about',   component: AboutPage,      meta: { headerVariant: 'inner' } },
  { path: '/monitor', component: MonitorPage,meta: { headerVariant: 'inner' } },
  { path: '/faq',     component: FaqPage,    meta: { headerVariant: 'inner' } },
  { path: '/contact', component: ContactPage,    meta: { headerVariant: 'inner' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

export default router
