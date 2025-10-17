<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <!-- Left Sidebar -->
    <LeftSidebar
      v-model:isOpen="isSidebarOpen"
      v-model:apiKey="apiKey"
      v-model:model="model"
      v-model:selectedProvider="selectedProvider"
      :systemPrompt="systemPrompt"
      :welcomePrompt="welcomePrompt"
      :isConnected="isConnected"
      :tokenUsage="tokenUsage"
      :isConnecting="isConnecting"
      @connectAPI="connectAPI"
      @clearAPI="clearAPI"
    />

    <!-- Main Chat Area -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300"
    >
      <!-- Header -->
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">🎙️ Speak with your AI assistant</div>
        </div>
        <div class="flex gap-2">
          <button
            v-for="btn in headerButtons"
            :key="btn.id"
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="btn.action"
          >
            {{ btn.label }}
          </button>
        </div>
      </div>

      <!-- Avatar moved here -->
      <div
        v-if="showAvatar"
        class="chat-avatar-container flex justify-center items-center py-4 border-b"
      >
        <AvatarComponent :state="avatarState" />
      </div>

      <!-- Messages -->
      <div ref="messagesContainer" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div v-for="(msg, i) in formattedMessages" :key="i" class="flex" :class="msg.align">
          <div
            class="max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="msg.style"
          >
            <div class="font-semibold text-xs mb-1">{{ msg.label }}</div>
            <div class="text-base whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.time }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <!-- Overlay if not connected -->
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect to Openrouter first
        </div>

        <!-- Mode Toggle -->
        <div class="flex justify-end mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-medium text-gray-700">Audio Mode</span>
            <button
              @click="toggleInputMode"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                inputMode === 'audio' ? 'bg-indigo-600' : 'bg-gray-200',
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  inputMode === 'audio' ? 'translate-x-6' : 'translate-x-1',
                ]"
              ></span>
            </button>
            <span class="text-sm font-medium text-gray-700">Text Mode</span>
          </div>
        </div>

        <!-- Audio Input -->
        <div v-if="inputMode === 'audio'">
          <div class="flex justify-center">
            <button
              class="px-6 py-3 rounded-full bg-red-500 text-white text-lg font-bold shadow-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
              :disabled="!isConnected || isPlaying || isRecognizing"
              @click="handleToggleRecording"
            >
              {{ isRecording ? "⏹ Listening" : "🎤 Speak" }}
            </button>

            <button
              class="px-6 py-3 rounded-full bg-green-600 text-white text-lg font-bold shadow-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed ml-4"
              :disabled="!chatHistory.length"
              @click="showReport = true"
              title="Finish & View Report"
            >
              ✓ Finish
            </button>
          </div>
        </div>

        <!-- Text Input -->
        <div v-else class="flex items-center space-x-2">
          <input
            v-model="userText"
            @keyup.enter="sendTextToChatbot"
            type="text"
            placeholder="Type your message..."
            class="flex-1 p-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow disabled:bg-gray-100"
            :disabled="!isConnected || isLoading"
          />
          <button
            @click="sendTextToChatbot"
            :disabled="!isConnected || !userText.trim() || isLoading"
            class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
          <button
            class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
            :disabled="!chatHistory.length"
            @click="showReport = true"
            title="Finish & View Report"
          >
            ✓
          </button>
        </div>
      </div>

      <!-- Report Modal -->
      <ReportModal
        :show="showReport"
        :chatHistory="chatHistory"
        :userCount="userCount"
        :assistantCount="assistantCount"
        :botName="selectedBot.name"
        @close="showReport = false"
      />
    </div>
  </div>

  <!-- Loader -->
  <div
    v-else
    class="flex h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500"
  >
    <div class="flex items-center space-x-3">
      <div class="h-8 w-8 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
      <span class="text-white text-2xl font-semibold"> Loading... </span>
    </div>
  </div>

  <!-- Notification -->
  <div
    v-if="notification.visible"
    class="fixed top-5 right-5 z-50 px-4 py-3 rounded-lg shadow-lg text-white"
    :class="notificationClass"
  >
    {{ notification.message }}
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "../components/text_chatbot/chatbotStore";
import { io } from "socket.io-client";
import { BASE_URL } from "../components/base_url";
import AvatarComponent from "../components/avatar/AvatarComponent.vue";
import LeftSidebar from "../components/avatar/LeftSidebar.vue";
import ReportModal from "../components/text_chatbot/ReportModal.vue";
import { useAzureSpeech } from "@/components/avatar/useAzureSpeech";

const props = defineProps({ avatarId: { type: String, required: true } });
const router = useRouter();
const chatbotStore = useChatbotStore();

// --- State ---
const chatHistory = ref([]);
const apiKey = ref("");
const systemPrompt = ref("");
const welcomePrompt = ref("");
const model = ref("");
const isConnected = ref(false);
const isSidebarOpen = ref(true);
const inputMode = ref("audio");
const userText = ref("");
const isLoading = ref(false);
const showReport = ref(false);
const selectedProvider = ref("openrouter");
const isConnecting = ref(false);
const notification = ref({ message: "", type: "success", visible: false });
const messagesContainer = ref(null);
const showAvatar = ref(true);

let socket = null;
const {
  isRecording,
  isPlaying,
  isRecognizing,
  avatarState,
  speakReplySequentially,
  toggleRecording,
  getAzureToken,
} = useAzureSpeech(showNotification);
// --- Computeds ---
const selectedBot = computed(() => chatbotStore.availableBots.find((b) => b.id === props.avatarId));
const assistantCount = computed(
  () => chatHistory.value.filter((m) => m.role === "assistant").length
);
const userCount = computed(() => chatHistory.value.filter((m) => m.role === "user").length);
const tokenUsage = computed(() => {
  let total = 0;
  chatHistory.value.forEach((m, i) => {
    if (m.role === "user") total += m.content?.length || 0;
    if (m.role === "assistant" && i !== 0) {
      total += m.content?.length || 0;
    }
  });
  return Math.floor((total * 3) / 4);
});

const formattedMessages = computed(() =>
  chatHistory.value.map((m) => ({
    ...m,
    align: m.role === "user" ? "justify-end" : "justify-start",
    style:
      m.role === "user"
        ? "bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none"
        : "bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none",
    label: m.role === "user" ? "👤 You" : "🤖 Assistant",
    time: m.timestamp.toLocaleTimeString(),
  }))
);

const notificationClass = computed(() =>
  notification.value.type === "success" ? "bg-green-500" : "bg-red-500"
);
const headerButtons = [
  {
    id: "left",
    label: computed(() => (isSidebarOpen.value ? "⬅ Hide Left" : "➡ Show Left")),
    action: () => (isSidebarOpen.value = !isSidebarOpen.value),
  },
  {
    id: "up",
    label: computed(() => (showAvatar.value ? "⬆️ Hide Avatar" : "⬇️ Show Avatar")),
    action: () => (showAvatar.value = !showAvatar.value),
  },
  { id: "new", label: "🔄 New Session", action: () => startNewSession() },
  { id: "back", label: "⬅ Back", action: () => goBack() },
];

// --- Lifecycle ---
onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedBot.value) {
    router.push("/");
    return;
  }

  systemPrompt.value =
    "Respond in plain text only — do not use Markdown, code blocks, or bold text. Keep your reply under 2 sentences. Additionally, follow these instructions: " +
    selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;
  await getAzureToken();
  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true);
  }
});
function sendTextToChatbot() {
  return sendMessage(userText.value, "text");
}

function handleToggleRecording() {
  toggleRecording((recognizedText) => sendMessage(recognizedText, "audio"));
}

async function sendMessage(text, via = "text") {
  if (!isConnected.value || !text.trim()) return;

  chatHistory.value.push(newMessage("user", text.trim()));
  chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."));
  const idx = chatHistory.value.length - 1;

  try {
    let reply;
    if (via === "text") {
      isLoading.value = true;
      avatarState.value = "thinking";
      const providerUrl = "/chatbot/chat_openrouter";
      const data = await apiCall(providerUrl, {
        chat_history: [
          { role: "system", content: systemPrompt.value },
          ...chatHistory.value.map(({ role, content }) => ({ role, content })),
        ],
        api_key: apiKey.value,
        model_name: model.value,
      });
      reply = data?.choices?.[0]?.message?.content || data?.error || "[No response]";
    } else {
      chatHistory.value[idx].content = "⏳ Avatar is thinking...";
      socket.emit("user_message", {
        text,
        system_prompt: systemPrompt.value,
        api_key: apiKey.value,
        model: model.value,
        provider: selectedProvider.value,
        history: chatHistory.value.map(({ role, content }) => ({ role, content })),
      });
      reply = await new Promise((resolve) =>
        socket.once("assistant_reply", (res) => resolve(res?.content || "[No response]"))
      );
    }

    chatHistory.value[idx] = newMessage("assistant", reply);
    scrollToBottom();
    await speakReplySequentially(reply);
  } catch (e) {
    console.error(e);
    chatHistory.value[idx] = newMessage(
      "assistant",
      "❌ Sorry, an error occurred. Please try again."
    );
  } finally {
    isLoading.value = false;
    avatarState.value = "idle";
  }
}
// --- Helpers ---
const newMessage = (role, content) => ({ role, content, timestamp: new Date() });
function scrollToBottom() {
  nextTick(() => {
    const el = messagesContainer.value;
    if (el) el.scrollTop = el.scrollHeight;
  });
}
function goBack() {
  router.push("/");
}
function toggleInputMode() {
  inputMode.value = inputMode.value === "audio" ? "text" : "audio";
}
function showNotification(msg, type = "success") {
  console.log(msg);
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
}
async function apiCall(endpoint, payload) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// --- API Connect ---
async function connectAPI(auto = false) {
  if (!apiKey.value && !auto && selectedProvider.value !== "openrouter") return;
  localStorage.setItem("chatbot_api_key", apiKey.value);
  isConnecting.value = true;
  isConnected.value = false;
  try {
    let providerUrl =
      selectedProvider.value === "openrouter" ? "/chatbot/chat_openrouter" : "/chatbot/chat";
    const data = await apiCall(providerUrl, {
      chat_history: [
        { role: "system", content: "connection test, return 1 if you can read." },
        { role: "user", content: "Hello!" },
      ],
      api_key: apiKey.value,
      model_name: model.value,
    });
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message;
    if (reply?.trim()) {
      isConnected.value = true;
      showNotification("✅ Connected and working!");
    } else {
      showNotification("⚠️ Connected, but no valid reply.", "error");
    }
  } catch (e) {
    console.error(e);
    showNotification("❌ Failed to connect.", "error");
  } finally {
    isConnecting.value = false;
  }
  connectWebSocket();
  if (!chatHistory.value.length && isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}
function clearAPI() {
  localStorage.removeItem("chatbot_api_key");
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
}

// --- WebSocket ---
function connectWebSocket() {
  socket = io(`${BASE_URL}/streaming-avatar`, { transports: ["websocket"] });
  socket.on("connect", () => console.log("WebSocket connected"));
}

// --- Chat Actions ---
function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
  }
}
</script>
