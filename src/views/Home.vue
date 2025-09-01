<template>
  <div
    class="flex h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <div class="bg-white/90 backdrop-blur-xl p-10 rounded-2xl shadow-2xl space-y-6 w-full max-w-lg">
      <h1 class="text-2xl font-bold text-center text-indigo-700">
        🤖 Choose Your Chatbot
      </h1>
      <p class="text-center text-gray-500">
        Select a chatbot to start a conversation.
      </p>

      <div class="space-y-4">
        <!-- Loop through available bots from the store -->
        <button
          v-for="bot in chatbotStore.availableBots"
          :key="bot.id"
          :class="['w-full p-5 rounded-xl bg-gradient-to-r text-white font-semibold shadow hover:opacity-90 transition', bot.styleClass]"
          @click="chooseBot(bot)"
        >
          {{ bot.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue' // <-- Import onMounted
import { useRouter } from 'vue-router'
import { useChatbotStore } from '../components/chatbotStore'

const router = useRouter()
const chatbotStore = useChatbotStore()

// When the component is first created, tell the store to load the bots.
onMounted(() => {
  chatbotStore.loadBots()
})

// This function is now much simpler!
function chooseBot(bot) {
  // The entire bot object (with name, prompts, model, etc.) is passed to the store
  chatbotStore.selectBot(bot)
  router.push('/chat')
}
</script>