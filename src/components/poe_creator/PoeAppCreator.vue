<template>
  <div class="poe-app-creator">
    <div class="header">
      <h2>🤖 Poe App Creator</h2>
      <div class="status-indicator" :class="{ connected: isConnected, disconnected: !isConnected }">
        {{ isConnected ? '🟢 Connected' : '🔴 Disconnected' }}
      </div>
    </div>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="{ active: activeTab === tab.id }"
        class="tab-button"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Chat Tab -->
    <div v-if="activeTab === 'chat'" class="tab-content">
      <div class="chat-container">
        <div class="messages" ref="messagesContainer">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', message.type]"
          >
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
        <div class="input-container">
          <textarea
            v-model="chatMessage"
            @keydown.enter.prevent="sendChatMessage"
            placeholder="Ask Poe App Creator anything..."
            rows="3"
          ></textarea>
          <button @click="sendChatMessage" :disabled="!chatMessage.trim() || isLoading">
            {{ isLoading ? 'Sending...' : 'Send' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Create App Tab -->
    <div v-if="activeTab === 'create-app'" class="tab-content">
      <div class="form-container">
        <div class="form-group">
          <label>App Description:</label>
          <textarea
            v-model="appDescription"
            placeholder="Describe the app you want to create..."
            rows="4"
          ></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>App Type:</label>
            <select v-model="appType">
              <option value="web_app">Web Application</option>
              <option value="mobile_app">Mobile Application</option>
              <option value="desktop_app">Desktop Application</option>
              <option value="api">API Service</option>
            </select>
          </div>
          <div class="form-group">
            <label>Framework:</label>
            <select v-model="framework">
              <option value="vue">Vue.js</option>
              <option value="react">React</option>
              <option value="angular">Angular</option>
              <option value="svelte">Svelte</option>
              <option value="vanilla">Vanilla JS</option>
            </select>
          </div>
        </div>
        <button @click="createApp" :disabled="!appDescription.trim() || isLoading" class="create-button">
          {{ isLoading ? 'Creating...' : 'Create App' }}
        </button>
        <div v-if="appResponse" class="response-container">
          <h3>App Creation Response:</h3>
          <pre>{{ JSON.stringify(appResponse, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- Code Review Tab -->
    <div v-if="activeTab === 'review'" class="tab-content">
      <div class="form-container">
        <div class="form-group">
          <label>Code to Review:</label>
          <textarea
            v-model="codeToReview"
            placeholder="Paste your code here for review..."
            rows="8"
          ></textarea>
        </div>
        <div class="form-group">
          <label>Programming Language:</label>
          <select v-model="codeLanguage">
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="vue">Vue.js</option>
            <option value="react">React JSX</option>
          </select>
        </div>
        <button @click="reviewCode" :disabled="!codeToReview.trim() || isLoading" class="review-button">
          {{ isLoading ? 'Reviewing...' : 'Review Code' }}
        </button>
        <div v-if="reviewResponse" class="response-container">
          <h3>Code Review:</h3>
          <pre>{{ JSON.stringify(reviewResponse, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- Component Generator Tab -->
    <div v-if="activeTab === 'generate'" class="tab-content">
      <div class="form-container">
        <div class="form-group">
          <label>Component Description:</label>
          <textarea
            v-model="componentDescription"
            placeholder="Describe the component you want to generate..."
            rows="4"
          ></textarea>
        </div>
        <div class="form-group">
          <label>Framework:</label>
          <select v-model="componentFramework">
            <option value="vue">Vue.js</option>
            <option value="react">React</option>
            <option value="angular">Angular</option>
            <option value="svelte">Svelte</option>
          </select>
        </div>
        <button @click="generateComponent" :disabled="!componentDescription.trim() || isLoading" class="generate-button">
          {{ isLoading ? 'Generating...' : 'Generate Component' }}
        </button>
        <div v-if="componentResponse" class="response-container">
          <h3>Generated Component:</h3>
          <pre>{{ JSON.stringify(componentResponse, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PoeAppCreator',
  data() {
    return {
      isConnected: false,
      isLoading: false,
      activeTab: 'chat',

      // Chat
      messages: [],
      chatMessage: '',

      // Create App
      appDescription: '',
      appType: 'web_app',
      framework: 'vue',
      appResponse: null,

      // Code Review
      codeToReview: '',
      codeLanguage: 'javascript',
      reviewResponse: null,

      // Component Generation
      componentDescription: '',
      componentFramework: 'vue',
      componentResponse: null,

      tabs: [
        { id: 'chat', label: '💬 Chat' },
        { id: 'create-app', label: '🚀 Create App' },
        { id: 'review', label: '🔍 Code Review' },
        { id: 'generate', label: '⚡ Generate Component' }
      ]
    }
  },

  mounted() {
    this.checkConnection()
  },

  methods: {
    async checkConnection() {
      try {
        const response = await fetch('http://localhost:5001/api/health')
        const data = await response.json()
        this.isConnected = data.client_status === 'ready'
      } catch (error) {
        console.error('Connection check failed:', error)
        this.isConnected = false
      }
    },

    async sendChatMessage() {
      if (!this.chatMessage.trim()) return

      // Add user message
      this.addMessage('user', this.chatMessage)
      const userMessage = this.chatMessage
      this.chatMessage = ''
      this.isLoading = true

      try {
        const response = await fetch('http://localhost:5001/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: userMessage,
            bot: 'App-Creator'
          })
        })

        const data = await response.json()

        if (data.success) {
          this.addMessage('bot', data.message)
        } else {
          this.addMessage('error', `Error: ${data.error || 'Unknown error'}`)
        }
      } catch (error) {
        console.error('Chat error:', error)
        this.addMessage('error', `Connection error: ${error.message}`)
      } finally {
        this.isLoading = false
      }
    },

    async createApp() {
      if (!this.appDescription.trim()) return

      this.isLoading = true
      this.appResponse = null

      try {
        const response = await fetch('http://localhost:5001/api/create-app', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            description: this.appDescription,
            type: this.appType,
            framework: this.framework
          })
        })

        this.appResponse = await response.json()
      } catch (error) {
        console.error('Create app error:', error)
        this.appResponse = { error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    async reviewCode() {
      if (!this.codeToReview.trim()) return

      this.isLoading = true
      this.reviewResponse = null

      try {
        const response = await fetch('http://localhost:5001/api/review-code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            code: this.codeToReview,
            language: this.codeLanguage
          })
        })

        this.reviewResponse = await response.json()
      } catch (error) {
        console.error('Code review error:', error)
        this.reviewResponse = { error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    async generateComponent() {
      if (!this.componentDescription.trim()) return

      this.isLoading = true
      this.componentResponse = null

      try {
        const response = await fetch('http://localhost:5001/api/generate-component', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            description: this.componentDescription,
            framework: this.componentFramework
          })
        })

        this.componentResponse = await response.json()
      } catch (error) {
        console.error('Component generation error:', error)
        this.componentResponse = { error: error.message }
      } finally {
        this.isLoading = false
      }
    },

    addMessage(type, content) {
      this.messages.push({
        id: Date.now(),
        type,
        content,
        timestamp: new Date()
      })

      this.$nextTick(() => {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight
        }
      })
    },

    formatTime(timestamp) {
      return timestamp.toLocaleTimeString()
    }
  }
}
</script>

<style scoped>
.poe-app-creator {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

.header h2 {
  margin: 0;
  color: #333;
}

.status-indicator {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.connected {
  background-color: #d4edda;
  color: #155724;
}

.disconnected {
  background-color: #f8d7da;
  color: #721c24;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background-color: #f5f5f5;
}

.tab-button.active {
  border-bottom-color: #007bff;
  color: #007bff;
  font-weight: bold;
}

.tab-content {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  min-height: 400px;
}

/* Chat Styles */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  padding: 10px;
  background-color: white;
  border-radius: 5px;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
}

.message.user {
  background-color: #007bff;
  color: white;
  margin-left: 20%;
}

.message.bot {
  background-color: #e9ecef;
  color: #333;
  margin-right: 20%;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message-content {
  word-wrap: break-word;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 5px;
}

.input-container {
  display: flex;
  gap: 10px;
}

.input-container textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
}

.input-container button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.input-container button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

/* Form Styles */
.form-container {
  max-width: 800px;
}

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
}

.create-button,
.review-button,
.generate-button {
  padding: 12px 30px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.create-button:disabled,
.review-button:disabled,
.generate-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.response-container {
  margin-top: 20px;
  padding: 15px;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.response-container h3 {
  margin-top: 0;
  color: #333;
}

.response-container pre {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 3px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>