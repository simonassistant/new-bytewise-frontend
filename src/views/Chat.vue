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
          <h1 class="text-xl font-bold">HKBU Learning Assistant</h1>
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
            v-model="messageInput"
            :disabled="!isConnected"
            placeholder="Type your message..."
            rows="1"
            class="chat-input flex-1 rounded-full border p-3 text-sm resize-none focus:ring focus:ring-indigo-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
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
    <div
      v-if="showReport"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        class="report-content bg-white w-full max-w-2xl rounded-lg shadow-xl p-6"
      >
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <h2 class="text-lg font-bold">📊 Learning Session Report</h2>
          <button class="close-btn" @click="showReport = false">&times;</button>
        </div>
        <div class="report-body space-y-2 max-h-96 overflow-y-auto text-sm">
          <p><strong>Total messages:</strong> {{ chatHistory.length }}</p>
          <p><strong>User messages:</strong> {{ userCount }}</p>
          <p><strong>Assistant messages:</strong> {{ assistantCount }}</p>
        </div>
        <div class="report-footer mt-4 flex justify-end gap-2">
          <button
            class="btn-secondary px-4 py-2 rounded-lg"
            @click="showReport = false"
          >
            Close
          </button>
        </div>
      </div>
    </div>

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
import { useChatbotStore } from "../components/chatbotStore";

const chatbotStore = useChatbotStore();

// ✅ Load selected bot
const selectedBot = chatbotStore.selectedBot;

// Fallback if no bot selected
if (!selectedBot) {
  window.location.href = "/";
}

const chatHistory = ref([]);
const notifications = ref([]);
const apiKey = ref("");
const systemPrompt = ref(selectedBot.systemPrompt);
const welcomePrompt = ref(selectedBot.welcomePrompt);
const model = ref(selectedBot.model);
const isConnected = ref(false);
const messageInput = ref("");
const showReport = ref(false);
const isSidebarOpen = ref(true);

const STORAGE_KEY = "chatHistory";

// ✅ Load history from localStorage on mount
onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY);
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
  window.history.back();
}
// ✅ Watch chatHistory and save to localStorage
watch(
  chatHistory,
  (newHistory) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newHistory));
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
    content: welcomePrompt.value,
    timestamp: new Date(),
  });
  notify("API connected successfully!", "success");
}

function clearAPI() {
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
  localStorage.removeItem(STORAGE_KEY);
  notify("API disconnected", "info");
}

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
          model: model.value,
          systemPrompt: systemPrompt.value,
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
  chatHistory.value = [];
  localStorage.removeItem(STORAGE_KEY);
  notify("Started new session", "success");
}

function notify(msg, type = "info") {
  const id = Date.now();
  notifications.value.push({ id, msg, type });
  setTimeout(() => {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  }, 3000);
}
</script>
