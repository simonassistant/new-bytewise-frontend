import { createRouter, createWebHistory } from 'vue-router'
import NewEEGC from '@/views/NewEEGC.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  {
    path: '/',
    redirect: '/eegc'
  },
  {
    path: '/eegc',
    name: 'EEGC',
    component: NewEEGC
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
