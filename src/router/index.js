// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Import the components you want to route to
import Home from '../views/Home.vue'
import Chat from '../views/Chat.vue'

// Define your routes
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/chat', name: 'Chat', component: Chat }
]

// Create router instance
const router = createRouter({
  history: createWebHistory(), // uses HTML5 history mode
  routes
})

export default router