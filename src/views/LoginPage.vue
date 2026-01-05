<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-100 via-white to-purple-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">EEGC Essay Tutor</h1>
        <p class="text-gray-600">Sign in to access the essay revision assistant</p>
      </div>

      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Your Name</label>
          <input
            v-model="name"
            type="text"
            placeholder="Enter your name..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="your.email@example.com"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">I am a...</label>
          <div class="grid grid-cols-2 gap-4">
            <button
              @click="selectedRole = 'student'"
              :class="[
                'p-4 rounded-lg border-2 transition-all duration-200 flex flex-col items-center',
                selectedRole === 'student' 
                  ? 'border-indigo-500 bg-indigo-50 text-indigo-700' 
                  : 'border-gray-200 hover:border-gray-300 text-gray-600'
              ]"
            >
              <span class="text-3xl mb-2">🎓</span>
              <span class="font-medium">Student</span>
            </button>
            <button
              @click="selectedRole = 'teacher'"
              :class="[
                'p-4 rounded-lg border-2 transition-all duration-200 flex flex-col items-center',
                selectedRole === 'teacher' 
                  ? 'border-indigo-500 bg-indigo-50 text-indigo-700' 
                  : 'border-gray-200 hover:border-gray-300 text-gray-600'
              ]"
            >
              <span class="text-3xl mb-2">👨‍🏫</span>
              <span class="font-medium">Teacher</span>
            </button>
          </div>
        </div>

        <div v-if="errorMessage" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {{ errorMessage }}
        </div>

        <button
          @click="handleLogin"
          :disabled="!canLogin || isLoading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <span v-if="isLoading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>

        <p class="text-center text-sm text-gray-500 mt-4">
          This is a demo login. OAuth integration with auth.hkbu.tech coming soon.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const name = ref('')
const email = ref('')
const selectedRole = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const canLogin = computed(() => {
  return name.value.trim() && email.value.trim() && selectedRole.value
})

async function handleLogin() {
  if (!canLogin.value || isLoading.value) return
  
  isLoading.value = true
  errorMessage.value = ''
  
  const result = await authStore.login({
    name: name.value.trim(),
    email: email.value.trim(),
    role: selectedRole.value
  })

  isLoading.value = false

  if (result.success) {
    if (selectedRole.value === 'teacher') {
      router.push('/dashboard')
    } else {
      router.push('/eegc')
    }
  } else {
    errorMessage.value = result.error || 'Login failed. Please try again.'
  }
}
</script>
