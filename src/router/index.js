// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomePage.vue'
import Chat from '../views/ChatPage.vue'
import Avatar from '../views/AvatarPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    // This is the new dynamic route.
    // It captures part of the URL as a variable named 'botId'.
    path: '/chat/:botId',
    name: 'Chat',
    component: Chat,
    // We pass the route params (like botId) as props to the component.
    props: true
  },
  {
    // This is the new dynamic route.
    // It captures part of the URL as a variable named 'botId'.
    path: '/avatar/:avatarId',
    name: 'Avatar',
    component: Avatar,
    // We pass the route params (like botId) as props to the component.
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
