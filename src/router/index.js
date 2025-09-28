// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomePage.vue'
import Chat from '../views/ChatPage.vue'
import Avatar from '../views/AvatarPage.vue'
import WritingBot from '../views/WritingBot.vue'
import PoeCreator from '../components/poe_creator/PoeAppCreator.vue'

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
    path: '/writingBot',
    name: 'WritingBot',
    component: WritingBot
  },
  {
    path: '/poe-creator',
    name: 'PoeCreator',
    component: PoeCreator
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
