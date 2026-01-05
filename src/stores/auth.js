import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')
  const currentSessionId = ref(null)

  async function login(userData) {
    try {
      const response = await axios.post('/api/db/users', {
        username: userData.name || userData.email,
        role: userData.role
      })
      
      user.value = {
        id: response.data.id,
        name: userData.name || response.data.username,
        email: userData.email,
        role: response.data.role,
        loginTime: new Date().toISOString()
      }
      localStorage.setItem('eegc_user', JSON.stringify(user.value))
      return user.value
    } catch (error) {
      console.error('Login error:', error)
      user.value = {
        id: `user_${Date.now()}`,
        name: userData.name,
        email: userData.email,
        role: userData.role,
        loginTime: new Date().toISOString()
      }
      localStorage.setItem('eegc_user', JSON.stringify(user.value))
      return user.value
    }
  }

  function logout() {
    user.value = null
    currentSessionId.value = null
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

  async function createChatSession(title = 'New Chat') {
    if (!user.value?.id) return null
    try {
      const response = await axios.post('/api/db/sessions', {
        user_id: user.value.id,
        title
      })
      currentSessionId.value = response.data.id
      return response.data
    } catch (error) {
      console.error('Create session error:', error)
      return null
    }
  }

  async function saveMessage(role, content) {
    if (!currentSessionId.value) return null
    try {
      const response = await axios.post('/api/db/messages', {
        session_id: currentSessionId.value,
        role,
        content
      })
      return response.data
    } catch (error) {
      console.error('Save message error:', error)
      return null
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
    isAuthenticated,
    isTeacher,
    isStudent,
    currentSessionId,
    login,
    logout,
    initFromStorage,
    createChatSession,
    saveMessage,
    getUserSessions,
    getSessionMessages
  }
})
