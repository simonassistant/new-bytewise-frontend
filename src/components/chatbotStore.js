// stores/chatbotStore.js
import { defineStore } from 'pinia'

export const useChatbotStore = defineStore('chatbot', {
  state: () => ({
    selectedBot: null
  }),
  actions: {
    selectBot(bot) {
      this.selectedBot = bot
    }
  }
})