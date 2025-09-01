<template>
  <div
    class="flex h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <div class="bg-white/90 backdrop-blur-xl p-10 rounded-2xl shadow-2xl space-y-6 w-full max-w-lg">
      <h1 class="text-2xl font-bold text-center text-indigo-700">
        🤖 Choose Your Chatbot
      </h1>
      <p class="text-center text-gray-500">
        Select a chatbot to start chatting with its custom prompts.
      </p>

      <div class="space-y-4">
        <button
          class="w-full p-5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold shadow hover:opacity-90 transition"
          @click="chooseBot('learning')"
        >
          🎓 Learning Assistant
        </button>

        <button
          class="w-full p-5 rounded-xl bg-gradient-to-r from-pink-500 to-red-500 text-white font-semibold shadow hover:opacity-90 transition"
          @click="chooseBot('fun')"
        >
          🎉 Fun Bot
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useChatbotStore } from '../components/chatbotStore'

const router = useRouter()
const chatbotStore = useChatbotStore()

function chooseBot(type) {
  if (type === 'learning') {
    chatbotStore.selectBot({
      name: "Learning Assistant",
      welcomePrompt: "Welcome to HKBU Chat Assistant!",
      systemPrompt: "You are a helpful AI learning assistant at HKBU.",
      model: "gpt-4.1-mini"
    })
  } else if (type === 'fun') {
    chatbotStore.selectBot({
      name: "Fun Bot",
      welcomePrompt: "Hey there! 🎉 Ready for some fun?",
      systemPrompt: "You are a witty, playful chatbot that tells jokes and entertains.",
      model: "gpt-3.5-turbo"
    })
  }

  router.push('/chat')
}
</script>