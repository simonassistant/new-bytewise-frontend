<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Teacher Dashboard</h1>
          <p class="text-gray-600">Welcome, {{ authStore.user?.name }}</p>
        </div>
        <div class="flex gap-4">
          <button
            @click="router.push('/eegc')"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Open EEGC Tutor
          </button>
          <button
            @click="handleLogout"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Total Students</h3>
          <p class="text-3xl font-bold text-indigo-600">{{ students.length }}</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Chat Sessions</h3>
          <p class="text-3xl font-bold text-green-600">{{ totalSessions }}</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Pending Reviews</h3>
          <p class="text-3xl font-bold text-orange-600">{{ pendingReviews }}</p>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Student Chat History</h2>
        </div>
        
        <div v-if="students.length === 0" class="p-8 text-center text-gray-500">
          <p class="text-lg mb-2">No student sessions yet</p>
          <p class="text-sm">Student chat histories will appear here once they start using the EEGC tutor.</p>
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="student in students"
            :key="student.id"
            class="p-6 hover:bg-gray-50 transition cursor-pointer"
            @click="openStudentHistory(student)"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ student.name }}</h3>
                <p class="text-gray-600">{{ student.email }}</p>
                <p class="text-sm text-gray-500 mt-1">
                  {{ student.sessions }} session(s) | Last active: {{ student.lastActive }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <span 
                  v-if="student.hasUnreviewed"
                  class="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full"
                >
                  Needs Review
                </span>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <StudentHistoryModal
        v-if="selectedStudent"
        :student="selectedStudent"
        @close="selectedStudent = null"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import StudentHistoryModal from '@/components/dashboard/StudentHistoryModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const selectedStudent = ref(null)

const students = ref([
  {
    id: 'demo_1',
    name: 'Demo Student',
    email: 'demo@student.edu',
    sessions: 3,
    lastActive: '2 hours ago',
    hasUnreviewed: true
  }
])

const totalSessions = computed(() => {
  return students.value.reduce((sum, s) => sum + s.sessions, 0)
})

const pendingReviews = computed(() => {
  return students.value.filter(s => s.hasUnreviewed).length
})

function openStudentHistory(student) {
  selectedStudent.value = student
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
