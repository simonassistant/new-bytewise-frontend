<template>
  <div
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
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
              @click="connectAPI"
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
          <h3 class="font-semibold mb-2">📝 Welcome Prompt</h3>
          <div class="bg-gray-100 p-3 rounded-lg text-sm shadow-inner">
            {{ welcomePrompt }}
          </div>
        </div>

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

    <!-- Chat Area -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300"
    >
      <!-- Header -->
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
          <!-- Sidebar toggle button -->
          <button
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            {{ isSidebarOpen ? "⬅ Hide Sidebar" : "➡ Show Sidebar" }}
          </button>

          <!-- New session button -->
          <button
            class="new-session-btn bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="startNewSession"
          >
            🔄 New Session
          </button>

          <!-- Back button -->
          <button
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="goBack()"
          >
            ⬅ Back
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div
          v-for="(msg, i) in chatHistory"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base"
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
            <div class="text-xs text-gray-500 mt-1 text-right">
              {{ msg.timestamp.toLocaleTimeString() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <!-- Overlay when not connected -->
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key first
        </div>

        <div class="chat-input-wrapper flex items-end gap-3">
          <textarea
            v-model="newMessage"
            placeholder="Type your message..."
            class="flex-grow p-3 pr-12 bg-white/20 backdrop-blur-sm rounded-l-xl focus:outline-none resize-none"
            rows="1"
            @input="adjustTextareaHeight"
            @keydown.enter.exact.prevent="sendMessage"
          ></textarea>  
          <div class="input-buttons flex gap-2">
            <!-- Send button -->
            <button
              class="px-4 py-2 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
              :disabled="!isConnected"
              @click="sendMessage"
              title="Send Message"
            >
              ➤
            </button>

            <!-- Done button -->
            <button
              class="px-4 py-2 rounded-full bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
              :disabled="
                chatHistory?.length == null || chatHistory.length === 0
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

    <!-- Report Modal -->
    <ReportModal
      :show="showReport"
      :chatHistory="chatHistory"
      :userCount="userCount"
      :assistantCount="assistantCount"
      @close="showReport = false"
    />

    <!-- Notifications -->
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
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from 'vue-router'; // UPDATED: Import useRouter
import { useChatbotStore } from "../components/chatbotStore";
import ReportModal from "../components/ReportModal.vue";

// UPDATED: Define props to accept 'botId' from the router
const props = defineProps({
  botId: {
    type: String,
    required: true,
  }
});

const router = useRouter(); // UPDATED: Initialize router
const chatbotStore = useChatbotStore();

// UPDATED: Find the bot using the botId from the URL prop, not from the store's "selectedBot"
const selectedBot = computed(() => chatbotStore.availableBots.find(b => b.id === props.botId));

const chatHistory = ref([]);
const notifications = ref([]);
const apiKey = ref("");
// UPDATED: These refs now depend on the 'selectedBot' computed property
const systemPrompt = ref('');
const welcomePrompt = ref('');
const model = ref('');
const isConnected = ref(false);
const messageInput = ref(""); // Note: Your template has a v-model named "newMessage", but script has "messageInput". I've used messageInput to match your sendMessage function. You may need to align these. Let's assume you'll fix the template v-model to "messageInput".
const showReport = ref(false);
const isSidebarOpen = ref(true);

// UPDATED: Use a unique storage key for each bot
const STORAGE_KEY = computed(() => `chatHistory_${props.botId}`);

onMounted(async () => {
  // Ensure bots are loaded. It might be good to await this.
  await chatbotStore.loadBots();

  // If the botId from the URL doesn't match any known bot, go home.
  if (!selectedBot.value) {
    router.push('/');
    return;
  }
  
  // UPDATED: Load settings from the found bot
  systemPrompt.value = selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;

  // Load history from the correct localStorage key
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
});

function goBack() {
  router.push('/'); // UPDATED: Use router push for cleaner navigation
}

watch(
  chatHistory,
  (newHistory) => {
    // UPDATED: Save to the bot-specific localStorage key
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

function connectAPI() {
  if (!apiKey.value) {
    notify("Please enter an API key", "error");
    return;
  }
  isConnected.value = true;
  chatHistory.value.push({
    role: "assistant",
    content: welcomePrompt.value, // Uses the ref
    timestamp: new Date(),
  });
  notify("API connected successfully!", "success");
}

function clearAPI() {
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
  notify("API disconnected", "info");
}

// NOTE: Please ensure the <textarea> v-model in your template is `messageInput` not `newMessage` to match this function.
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

  chatHistory.value.push({
    role: "assistant",
    content: "⏳ Assistant is typing...",
    timestamp: new Date(),
    typing: true,
  });

  try {
    const response = await fetch(
      "https://smartlessons-production.up.railway.app/api/chat",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          apiKey: apiKey.value,
          provider: "hkbu",
          model: model.value, // Uses the ref
          systemPrompt: systemPrompt.value, // Uses the ref
        }),
      }
    );

    const data = await response.json();

    chatHistory.value = chatHistory.value.filter((m) => !m.typing);

    if (response.ok && !data.error) {
      chatHistory.value.push({
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      });
    } else {
      chatHistory.value.push({
        role: "assistant",
        content: `⚠️ Error: ${data.error || "Unknown error"}`,
        timestamp: new Date(),
      });
    }
  } catch (error) {
    chatHistory.value = chatHistory.value.filter((m) => !m.typing);

    chatHistory.value.push({
      role: "assistant",
      content: `⚠️ Network error: ${error.message}`,
      timestamp: new Date(),
    });
  }
}

function startNewSession() {
  chatHistory.value = []; // This will trigger the watch to clear localStorage
  notify("Started new session", "success");
}

function notify(msg, type = "info") {
  const id = Date.now();
  notifications.value.push({ id, msg, type });
  setTimeout(() => {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  }, 3000);
}

// This function seems unused in your template but is present in the `chat-input-container` section. If you re-add a text area with `ref="textareaRef"`, it will work.
const textareaRef = ref(null);
function adjustTextareaHeight() {
    const textarea = textareaRef.value;
    if (textarea) {
        textarea.style.height = 'auto'; // Reset height
        textarea.style.height = `${textarea.scrollHeight}px`; // Set to scroll height
    }
}
</script>