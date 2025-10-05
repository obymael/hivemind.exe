import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AboutPage from '../views/AboutPage.vue'
import VegetationIndexPage from '../views/VegetationIndexPage.vue'
import MyGardenPage from '../views/MyGardenPage.vue'
import ContactPage from '../views/ContactPage.vue'

const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: '/about',   component: AboutPage,      meta: { headerVariant: 'inner' } },
  { path: '/monitor', component: VegetationIndexPage,meta: { headerVariant: 'inner' } },
  { path: '/mygarden', component: MyGardenPage,meta: { headerVariant: 'inner' } },
  { path: '/contact', component: ContactPage,    meta: { headerVariant: 'inner' } },
  { path: '/vegetation-index', name: 'VegetationIndex', component: VegetationIndexPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

export default router
