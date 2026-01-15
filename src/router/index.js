import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomePage.vue'
import ChatWorkspace from '../views/ChatWorkspace.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/chat/:appId',
    name: 'Chat',
    component: ChatWorkspace,
    props: true
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
