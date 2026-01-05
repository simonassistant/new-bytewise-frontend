import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')

  function login(userData) {
    user.value = {
      id: userData.id || `user_${Date.now()}`,
      name: userData.name,
      email: userData.email,
      role: userData.role,
      loginTime: new Date().toISOString()
    }
    localStorage.setItem('eegc_user', JSON.stringify(user.value))
  }

  function logout() {
    user.value = null
    localStorage.removeItem('eegc_user')
  }

  function initFromStorage() {
    const stored = localStorage.getItem('eegc_user')
    if (stored) {
      try {
        user.value = JSON.parse(stored)
      } catch {
        localStorage.removeItem('eegc_user')
      }
    }
  }

  return {
    user,
    isAuthenticated,
    isTeacher,
    isStudent,
    login,
    logout,
    initFromStorage
  }
})
