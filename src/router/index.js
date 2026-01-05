// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomePage.vue'
import Chat from '../views/ChatPage.vue'
import Avatar from '../views/AvatarPage.vue'
import WritingBot from '../views/WritingBot.vue'
// import CloseEEGC from '../views/ClouseEEGC.vue'
import NewEEGC from '@/views/NewEEGC.vue'
import ThreeBotsSimulation from '../views/ThreeBotsSimulation.vue'
import NotFound from '../views/NotFound.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/chat/:botId',
    name: 'Chat',
    component: Chat,
    props: true
  },
  {
    path: '/avatar/:avatarId',
    name: 'Avatar',
    component: Avatar,
    props: true
  },
  {
    path: '/EEGC',
    name: 'EEGC',
    component: NewEEGC
  },
  {
    path: '/old_EEGC',
    name: 'old_EEGC',
    component: WritingBot
  },
  {
    path: '/three-bots-simulation',
    name: 'ThreeBotsSimulation',
    component: ThreeBotsSimulation
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
