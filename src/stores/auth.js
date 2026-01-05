import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loginError = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')
  const currentSessionId = ref(null)

  async function login(userData) {
    loginError.value = null
    try {
      const response = await axios.post('/api/db/users', {
        username: userData.name || userData.email,
        role: userData.role
      })
      
      if (response.data.error) {
        throw new Error(response.data.error)
      }
      
      user.value = {
        id: response.data.id,
        name: userData.name || response.data.username,
        email: userData.email,
        role: response.data.role,
        loginTime: new Date().toISOString()
      }
      localStorage.setItem('eegc_user', JSON.stringify(user.value))
      return { success: true, user: user.value }
    } catch (error) {
      console.error('Login error:', error)
      loginError.value = error.response?.data?.error || error.message || 'Login failed'
      return { success: false, error: loginError.value }
    }
  }

  function logout() {
    user.value = null
    currentSessionId.value = null
    loginError.value = null
    localStorage.removeItem('eegc_user')
  }

  function guestLogin(role) {
    user.value = {
      id: `guest_${Date.now()}`,
      name: role === 'teacher' ? 'Guest Teacher' : 'Guest Student',
      email: `guest_${role}@demo.local`,
      role: role,
      isGuest: true,
      loginTime: new Date().toISOString()
    }
    localStorage.setItem('eegc_user', JSON.stringify(user.value))
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

  async function createChatSession(title = 'New Chat') {
    if (!user.value?.id) return { success: false, error: 'Not logged in' }
    try {
      const response = await axios.post('/api/db/sessions', {
        user_id: user.value.id,
        title
      })
      
      if (response.data.error) {
        throw new Error(response.data.error)
      }
      
      currentSessionId.value = response.data.id
      return { success: true, session: response.data }
    } catch (error) {
      console.error('Create session error:', error)
      return { success: false, error: error.response?.data?.error || error.message }
    }
  }

  async function saveMessage(role, content) {
    if (!currentSessionId.value) return { success: false, error: 'No active session' }
    try {
      const response = await axios.post('/api/db/messages', {
        session_id: currentSessionId.value,
        role,
        content
      })
      
      if (response.data.error) {
        throw new Error(response.data.error)
      }
      
      return { success: true, message: response.data }
    } catch (error) {
      console.error('Save message error:', error)
      return { success: false, error: error.response?.data?.error || error.message }
    }
  }

  async function getUserSessions() {
    if (!user.value?.id) return []
    try {
      const response = await axios.get(`/api/db/sessions/${user.value.id}`)
      return response.data
    } catch (error) {
      console.error('Get sessions error:', error)
      return []
    }
  }

  async function getSessionMessages(sessionId) {
    try {
      const response = await axios.get(`/api/db/messages/${sessionId}`)
      return response.data
    } catch (error) {
      console.error('Get messages error:', error)
      return []
    }
  }

  return {
    user,
    loginError,
    isAuthenticated,
    isTeacher,
    isStudent,
    currentSessionId,
    login,
    logout,
    guestLogin,
    initFromStorage,
    createChatSession,
    saveMessage,
    getUserSessions,
    getSessionMessages
  }
})
