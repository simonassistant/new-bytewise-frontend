<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-gray-900">{{ student.name }}'s Chat History</h2>
          <p class="text-gray-600 text-sm">{{ student.email }}</p>
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
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Sessions</h3>
          <div class="space-y-4">
            <div
              v-for="session in sessions"
              :key="session.id"
              class="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition cursor-pointer"
              :class="{ 'border-indigo-500 bg-indigo-50': selectedSession?.id === session.id }"
              @click="selectedSession = session"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-medium text-gray-900">{{ session.mode }} Mode</span>
                  <span class="text-gray-500 text-sm ml-2">{{ session.date }}</span>
                </div>
                <span class="text-sm text-gray-600">{{ session.messageCount }} messages</span>
              </div>
              <p class="text-sm text-gray-600 line-clamp-2">{{ session.preview }}</p>
            </div>
          </div>
        </div>

        <div v-if="selectedSession" class="border-t pt-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Chat Messages</h3>
          <div class="space-y-3 mb-6 max-h-64 overflow-y-auto">
            <div
              v-for="(msg, idx) in selectedSession.messages"
              :key="idx"
              :class="[
                'p-3 rounded-lg',
                msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'
              ]"
            >
              <p class="text-xs text-gray-500 mb-1">{{ msg.role === 'user' ? 'Student' : 'AI Tutor' }}</p>
              <p class="text-sm text-gray-800">{{ msg.content }}</p>
            </div>
          </div>

          <div class="border-t pt-4">
            <h4 class="font-medium text-gray-800 mb-2">Teacher Comments</h4>
            <div v-if="selectedSession.comments?.length" class="space-y-2 mb-4">
              <div
                v-for="(comment, idx) in selectedSession.comments"
                :key="idx"
                class="bg-yellow-50 border border-yellow-200 rounded-lg p-3"
              >
                <p class="text-sm text-gray-800">{{ comment.text }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ comment.date }}</p>
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
                :disabled="!newComment.trim()"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 transition"
              >
                Add Comment
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  student: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const selectedSession = ref(null)
const newComment = ref('')

const sessions = ref([
  {
    id: 'session_1',
    mode: 'Training',
    date: '2 hours ago',
    messageCount: 12,
    preview: 'Working on thesis statement revision for climate change essay...',
    messages: [
      { role: 'assistant', content: 'Welcome to the EEGC Training Mode! Let\'s work on improving your essay.' },
      { role: 'user', content: 'I need help with my thesis statement.' },
      { role: 'assistant', content: 'Great! A strong thesis statement should clearly state your main argument. Can you share your current thesis?' },
      { role: 'user', content: 'Climate change is bad and we should do something about it.' },
      { role: 'assistant', content: 'Your thesis needs to be more specific. Consider: What exactly should we do? Who should take action? Try revising it to include a clear stance and reasoning.' }
    ],
    comments: [
      { text: 'Good progress on thesis development. Encourage more specific language.', date: '1 hour ago' }
    ]
  },
  {
    id: 'session_2',
    mode: 'Assessment',
    date: 'Yesterday',
    messageCount: 8,
    preview: 'Essay assessment on migrant workers topic...',
    messages: [
      { role: 'assistant', content: 'Welcome to Assessment Mode. Please paste your essay for review.' },
      { role: 'user', content: 'Here is my essay about migrant workers...' },
      { role: 'assistant', content: 'Thank you for sharing. Let me analyze your essay structure and arguments.' }
    ],
    comments: []
  }
])

function addComment() {
  if (!newComment.value.trim() || !selectedSession.value) return
  
  if (!selectedSession.value.comments) {
    selectedSession.value.comments = []
  }
  
  selectedSession.value.comments.push({
    text: newComment.value.trim(),
    date: 'Just now'
  })
  
  newComment.value = ''
}
</script>
