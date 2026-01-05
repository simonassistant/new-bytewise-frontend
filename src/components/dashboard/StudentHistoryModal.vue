<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-gray-900">{{ student.username }}'s Chat History</h2>
          <p class="text-gray-600 text-sm">{{ student.session_count }} sessions</p>
        </div>
        <button
          @click="$emit('close')"
          class="p-2 hover:bg-gray-100 rounded-full transition"
        >
          <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <div v-if="loading" class="text-center text-gray-500 py-8">
          Loading sessions...
        </div>

        <div v-else-if="sessions.length === 0" class="text-center text-gray-500 py-8">
          <p>No chat sessions found for this student.</p>
        </div>

        <div v-else class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Sessions</h3>
          <div class="space-y-4">
            <div
              v-for="session in sessions"
              :key="session.id"
              class="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition cursor-pointer"
              :class="{ 'border-indigo-500 bg-indigo-50': selectedSession?.id === session.id }"
              @click="selectSession(session)"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-medium text-gray-900">{{ session.title }}</span>
                  <span class="text-gray-500 text-sm ml-2">{{ formatDate(session.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedSession" class="border-t pt-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Chat Messages</h3>
          
          <div v-if="loadingMessages" class="text-center text-gray-500 py-4">
            Loading messages...
          </div>
          
          <div v-else class="space-y-3 mb-6 max-h-64 overflow-y-auto">
            <div
              v-for="(msg, idx) in selectedSession.messages"
              :key="idx"
              :class="[
                'p-3 rounded-lg',
                msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'
              ]"
            >
              <p class="text-xs text-gray-500 mb-1">{{ msg.role === 'user' ? 'Student' : 'AI Tutor' }}</p>
              <p class="text-sm text-gray-800 whitespace-pre-wrap">{{ msg.content }}</p>
            </div>
          </div>

          <div class="border-t pt-4">
            <h4 class="font-medium text-gray-800 mb-2">Teacher Comments</h4>
            <div v-if="selectedSession.comments?.length" class="space-y-2 mb-4">
              <div
                v-for="comment in selectedSession.comments"
                :key="comment.id"
                class="bg-yellow-50 border border-yellow-200 rounded-lg p-3"
              >
                <p class="text-sm text-gray-800">{{ comment.comment }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ comment.teacher_name }} - {{ formatDate(comment.created_at) }}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newComment"
                type="text"
                placeholder="Add a comment..."
                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                @keyup.enter="addComment"
              />
              <button
                @click="addComment"
                :disabled="!newComment.trim() || savingComment"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 transition"
              >
                {{ savingComment ? 'Saving...' : 'Add Comment' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  student: {
    type: Object,
    required: true
  },
  teacherId: {
    type: [Number, String],
    default: null
  }
})

defineEmits(['close'])

const loading = ref(true)
const loadingMessages = ref(false)
const savingComment = ref(false)
const sessions = ref([])
const selectedSession = ref(null)
const newComment = ref('')

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

async function loadSessions() {
  loading.value = true
  try {
    const response = await axios.get(`/api/db/sessions/${props.student.id}`)
    sessions.value = response.data
  } catch (error) {
    console.error('Error loading sessions:', error)
    sessions.value = []
  } finally {
    loading.value = false
  }
}

async function selectSession(session) {
  selectedSession.value = { ...session, messages: [], comments: [] }
  loadingMessages.value = true
  
  try {
    const [messagesRes, commentsRes] = await Promise.all([
      axios.get(`/api/db/messages/${session.id}`),
      axios.get(`/api/db/comments/${session.id}`)
    ])
    selectedSession.value.messages = messagesRes.data
    selectedSession.value.comments = commentsRes.data
  } catch (error) {
    console.error('Error loading session details:', error)
  } finally {
    loadingMessages.value = false
  }
}

async function addComment() {
  if (!newComment.value.trim() || !selectedSession.value || !props.teacherId) return
  
  savingComment.value = true
  try {
    const response = await axios.post('/api/db/comments', {
      session_id: selectedSession.value.id,
      teacher_id: props.teacherId,
      comment: newComment.value.trim()
    })
    
    if (!selectedSession.value.comments) {
      selectedSession.value.comments = []
    }
    
    selectedSession.value.comments.unshift({
      id: response.data.id,
      comment: newComment.value.trim(),
      created_at: response.data.created_at,
      teacher_name: 'You'
    })
    
    newComment.value = ''
  } catch (error) {
    console.error('Error adding comment:', error)
  } finally {
    savingComment.value = false
  }
}

onMounted(() => {
  loadSessions()
})
</script>
