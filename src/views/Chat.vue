<template>
  <div v-if="selectedBot" class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800">
    <!-- Sidebar -->
    <aside
      class="bg-white/90 backdrop-blur shadow-xl flex flex-col transition-all duration-300 overflow-hidden"
      :class="isSidebarOpen ? 'w-80' : 'w-0'"
    >
      <!-- Header -->
      <div
        v-if="isSidebarOpen"
        class="p-5 border-b bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex justify-between items-center"
      >
        <h2 class="text-lg font-bold flex items-center gap-2">
          🤖 Chatbot Configuration
        </h2>
        <button
          class="text-white hover:text-gray-200"
          @click="isSidebarOpen = false"
        >
          ✖
        </button>
      </div>

      <!-- Content -->
      <div v-if="isSidebarOpen" class="p-5 space-y-6 flex-1 overflow-y-auto">
        <!-- API Config -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 class="font-semibold text-yellow-800 mb-3">
            🔑 API Configuration
          </h3>
          <input
            type="password"
            v-model="apiKey"
            placeholder="Paste your API key..."
            class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
          />

          <!-- ADDED: Instruction text with a link -->
          <p class="text-xs text-gray-600 mt-2">
            Get your key from the 
            <a 
              href="https://genai.hkbu.edu.hk/settings/api-docs" 
              target="_blank" 
              rel="noopener noreferrer"
              class="text-indigo-600 hover:underline"
            >
              HKBU Generative AI Platform
            </a>.
          </p>
          <!-- END ADDED -->

          <select
            v-model="model"
            class="w-full mt-3 border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
          >
            <option value="gpt-4.1-mini">GPT-4.1 Mini</option>
            <option value="gpt-4.1">GPT-4.1</option>
            <option value="gpt-4.1-turbo">GPT-4.1 Turbo</option>
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
          </select>
          <div class="flex gap-2 mt-3">
            <button
              class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium"
              @click="connectAPI()"
            >
              ✅ Connect
            </button>
            <button
              class="px-4 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 text-gray-700 text-sm font-medium"
              @click="clearAPI"
            >
              🗑️ Clear
            </button>
          </div>
        </div>

        <!-- Prompts -->
        <div>
          <h3 class="font-semibold mb-2">⚙️ System Prompt</h3>
          <div class="bg-gray-100 p-3 rounded-lg text-sm shadow-inner">
            {{ systemPrompt }}
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div
        v-if="isSidebarOpen"
        class="p-4 border-t text-xs text-gray-600 bg-gray-50 space-y-1"
      >
        <div class="font-semibold text-gray-800">Created by:</div>
        <div>Dr. Simon Wang</div>
        <div>Innovation Officer, Language Centre</div>
        <div>Hong Kong Baptist University</div>
        <div>
          📧
          <a
            href="mailto:simonwang@hkbu.edu.hk"
            class="text-indigo-600 hover:underline"
          >
            simonwang@hkbu.edu.hk
          </a>
        </div>
      </div>
    </aside>

    <!-- Chat Area (no changes here) -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300"
    >
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">
            💡 Customize prompts, chat, and generate learning reports
          </div>
        </div>
        <div class="flex gap-2">
          <button
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            {{ isSidebarOpen ? "⬅ Hide Sidebar" : "➡ Show Sidebar" }}
          </button>
          <button
            class="new-session-btn bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="startNewSession"
          >
            🔄 New Session
          </button>
          <button
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="goBack()"
          >
            ⬅ Back
          </button>
        </div>
      </div>
      <div class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div
          v-for="(msg, i) in chatHistory"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="
              msg.role === 'user'
                ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none'
                : 'bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none'
            "
          >
            <div class="font-semibold text-xs mb-1">
              {{ msg.role === "user" ? "👤 You" : "🤖 Assistant" }}
            </div>
            <div class="text-base whitespace-pre-wrap">
              {{ msg.content }}
            </div>
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.timestamp.toLocaleTimeString() }}
            </div>
          </div>
        </div>
      </div>
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key first
        </div>
        <div class="chat-input-wrapper flex items-end gap-3">
          <textarea
            v-model="messageInput"
            placeholder="Type your message..."
            class="flex-grow p-3 pr-4 bg-gray-100 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-300 resize-none"
            rows="1"
            ref="textareaRef"
            @input="adjustTextareaHeight"
            @keydown.enter.exact.prevent="sendMessage"
          ></textarea>
          <div class="input-buttons flex gap-2">
            <button
              class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
              :disabled="!isConnected"
              @click="sendMessage"
              title="Send Message"
            >
              ➤
            </button>
            <button
              class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
              :disabled="
                !chatHistory || chatHistory.length === 0
              "
              @click="showReport = true"
              title="Finish & View Report"
            >
              ✓
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modals (no changes here) -->
    <ReportModal
      :show="showReport"
      :chatHistory="chatHistory"
      :userCount="userCount"
      :assistantCount="assistantCount"
      :botName="selectedBot.name"
      @close="showReport = false"
    />
    <div class="fixed top-5 right-5 space-y-2 z-50">
      <div
        v-for="n in notifications"
        :key="n.id"
        class="px-4 py-3 rounded-lg shadow-lg text-white text-sm"
        :class="{
          'bg-blue-500': n.type === 'info',
          'bg-green-500': n.type === 'success',
          'bg-red-500': n.type === 'error',
        }"
      >
        {{ n.msg }}
      </div>
    </div>
  </div>

  <div v-else class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 items-center justify-center">
    <div class="flex items-center justify-center space-x-3">
      <svg class="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-white text-2xl font-semibold">Loading Chatbot...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from 'vue-router';
import { useChatbotStore } from "../components/chatbotStore";
import ReportModal from "../components/ReportModal.vue";

const props = defineProps({
  botId: {
    type: String,
    required: true,
  }
});

const router = useRouter();
const chatbotStore = useChatbotStore();

const selectedBot = computed(() => chatbotStore.availableBots.find(b => b.id === props.botId));

const chatHistory = ref([]);
const notifications = ref([]);
const apiKey = ref("");
const systemPrompt = ref('');
const welcomePrompt = ref('');
const model = ref('');
const isConnected = ref(false);
const messageInput = ref("");
const showReport = ref(false);
const isSidebarOpen = ref(true);

const STORAGE_KEY = computed(() => `chatHistory_${props.botId}`);
const API_KEY_STORAGE_KEY = 'chatbot_api_key';

// UPDATED onMounted with corrected order of operations
onMounted(async () => {
    
  // 1. Load bot configs FIRST, so we have the data we need.
  await chatbotStore.loadBots();

  // Redirect if the bot is not valid
  if (!selectedBot.value) {
    router.push('/');
    return;
  }
  
  // 2. Populate component state from the loaded bot config.
  // Now welcomePrompt.value will have the correct text.
  systemPrompt.value = selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;

  // 3. Load saved chat history.
  const saved = localStorage.getItem(STORAGE_KEY.value);
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      chatHistory.value = parsed.map((m) => ({
        ...m,
        timestamp: new Date(m.timestamp),
      }));
    } catch (e) {
      console.error("Failed to parse chat history:", e);
    }
  }

  // 4. NOW, with all other state loaded, try to auto-connect.
  // connectAPI() will now have the correct welcomePrompt and chatHistory status.
  const savedApiKey = localStorage.getItem(API_KEY_STORAGE_KEY);
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true); // pass a flag to suppress "already connected" notification
  }
});

function goBack() {
  router.push('/');
}

watch(
  chatHistory,
  (newHistory) => {
    if(newHistory.length > 0) {
      localStorage.setItem(STORAGE_KEY.value, JSON.stringify(newHistory));
    } else {
      localStorage.removeItem(STORAGE_KEY.value);
    }
  },
  { deep: true }
);

const userCount = computed(
  () => chatHistory.value.filter((m) => m.role === "user").length
);
const assistantCount = computed(
  () => chatHistory.value.filter((m) => m.role === "assistant").length
);

function connectAPI(isAutoConnect = false) {
  if (isConnected.value && !isAutoConnect) {
    notify("Already connected!", "info");
    return;
  }
  if (!apiKey.value) {
    if (!isAutoConnect) notify("Please enter an API key", "error");
    return;
  }
  
  localStorage.setItem(API_KEY_STORAGE_KEY, apiKey.value);

  isConnected.value = true;
  // This check now works correctly because chatHistory and welcomePrompt are already loaded.
  if (chatHistory.value.length === 0) {
    chatHistory.value.push({
      role: "assistant",
      content: welcomePrompt.value,
      timestamp: new Date(),
    });
  }
  if (!isAutoConnect) notify("API connected successfully!", "success");
}

function clearAPI() {
  localStorage.removeItem(API_KEY_STORAGE_KEY);
  
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
  notify("API disconnected", "info");
}

// PASTE THIS ENTIRE FUNCTION TO REPLACE YOUR OLD sendMessage

async function sendMessage() {
  if (!isConnected.value) {
    notify("Please connect your API key first", "error");
    return;
  }

  const message = messageInput.value.trim();
  if (!message) return;

  chatHistory.value.push({
    role: "user",
    content: message,
    timestamp: new Date(),
  });

  messageInput.value = "";
  // Auto-resize textarea after sending
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto';
  }


  chatHistory.value.push({
    role: "assistant",
    content: "⏳ Assistant is typing...",
    timestamp: new Date(),
    typing: true,
  });

  try {
    // 1. Prepare the message history for the API.
    // We remove the "typing" indicator and any other UI-specific fields.
    const messagesToSend = chatHistory.value
      .filter(m => !m.typing) // Don't send the "typing..." placeholder
      .map(m => ({ role: m.role, content: m.content })); // Send only role and content

    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/api/chat`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },

        // 2. ✅ SOLUTION: Send the entire message history
        body: JSON.stringify({
          // The 'message' property is replaced by the 'messages' array
          messages: messagesToSend, 
          apiKey: apiKey.value,
          provider: "hkbu",
          model: model.value,
          systemPrompt: systemPrompt.value,
        }),
      }
    );

    // Remove the "typing..." message from the UI
    chatHistory.value = chatHistory.value.filter((m) => !m.typing);
    
    // Check for network or server errors first
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response.' }));
        throw new Error(errorData.error || `Request failed with status ${response.status}`);
    }

    const data = await response.json();

    if (data.response) {
      chatHistory.value.push({
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      });
    } else {
      throw new Error(data.error || "Received an empty response from the server.");
    }
  } catch (error) {
    // Make sure typing indicator is removed even if there's an error
    chatHistory.value = chatHistory.value.filter((m) => !m.typing);
    chatHistory.value.push({
      role: "assistant",
      content: `⚠️ Error: ${error.message}`,
      timestamp: new Date(),
    });
  }
}

function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value) {
    chatHistory.value.push({
      role: "assistant",
      content: welcomePrompt.value,
      timestamp: new Date(),
    });
  }
  notify("Started new session", "success");
}

function notify(msg, type = "info") {
  const id = Date.now();
  notifications.value.push({ id, msg, type });
  setTimeout(() => {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  }, 3000);
}

const textareaRef = ref(null);
function adjustTextareaHeight() {
    const textarea = textareaRef.value;
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
    }
}
</script>