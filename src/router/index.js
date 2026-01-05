import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginPage from '@/views/LoginPage.vue'
import NewEEGC from '@/views/NewEEGC.vue'
import TeacherDashboard from '@/views/TeacherDashboard.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/eegc',
    name: 'EEGC',
    component: NewEEGC,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true, requiresTeacher: true }
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

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (!authStore.user) {
    authStore.initFromStorage()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    return next(authStore.isTeacher ? '/dashboard' : '/eegc')
  }

  if (to.meta.requiresTeacher && !authStore.isTeacher) {
    return next('/eegc')
  }

  next()
})

export default router
