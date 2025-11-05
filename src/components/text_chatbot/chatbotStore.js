import { defineStore } from 'pinia';

export const useChatbotStore = defineStore('chatbot', {
  state: () => ({
    selectedBot: null,
    availableBots: [],
    currentState: {
      mode: null,
      context: null,
    },
  }),

  actions: {
    selectBot(bot) {
      this.selectedBot = bot;
    },

    async loadBots() {
      if (this.availableBots.length > 0) return;

      // Grab all imports
      const modules = import.meta.glob('@/botConfig/*.json');

      // Kick off all imports in parallel
      const loadPromises = Object.entries(modules).map(async ([path, loader]) => {
        const module = await loader();
        const id = path.split('/').pop().replace('.json', '');
        return {
          id,
          ...module.default,
        };
      });

      // Wait for all to complete
      this.availableBots = await Promise.all(loadPromises);
    },

    setConversationState(mode, context = null) {
      this.currentState = {
        mode,
        context,
      };
    },

    getConversationState() {
      return this.currentState;
    },
  },
});
