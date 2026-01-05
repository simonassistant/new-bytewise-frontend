<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800 relative"
  >
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black/50 z-40 md:hidden"
      @click="isSidebarOpen = false"
    ></div>

    <!-- Left Sidebar -->
    <LeftSidebar
      v-model:isOpen="isSidebarOpen"
      @updateUserData="handleUserDataUpdate"
      :tokenUsage="tokenUsage"
      class="md:relative fixed md:z-auto z-50 h-full"
    />

    <!-- Main Chat Area -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300 w-full md:w-auto"
    >
      <!-- Header -->
      <div
        class="chat-header flex flex-col sm:flex-row justify-between items-start sm:items-center p-3 sm:p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white gap-3"
      >
        <div class="flex-1 min-w-0">
          <h1 class="text-lg sm:text-xl font-bold truncate">{{ selectedBot.name }}</h1>
          <div class="text-xs sm:text-sm opacity-80">🎙️ Speak with your AI assistant</div>
        </div>
        <div class="flex gap-1 sm:gap-2 flex-wrap">
          <button
            v-for="btn in headerButtons"
            :key="btn.id"
            class="bg-white/20 px-2 sm:px-3 py-1 rounded-lg hover:bg-white/30 text-xs sm:text-sm whitespace-nowrap"
            @click="btn.action"
          >
            {{ btn.label }}
          </button>
        </div>
      </div>

      <!-- Avatar moved here -->
      <div
        v-if="showAvatar"
        class="chat-avatar-container flex justify-center items-center py-2 sm:py-4 border-b"
      >
        <div class="w-32 h-32 sm:w-48 sm:h-48 md:w-64 md:h-64">
          <AvatarComponent :state="avatarState" :gender="avatarGender" :appearance="avatarAppearance" />
        </div>
      </div>

      <!-- Messages -->
      <div ref="messagesContainer" class="chat-messages flex-1 overflow-y-auto p-3 sm:p-5 space-y-3 sm:space-y-4">
        <div v-for="(msg, i) in formattedMessages" :key="i" class="flex" :class="msg.align">
          <div
            class="max-w-[85%] sm:max-w-2xl md:max-w-3xl px-3 sm:px-4 py-2 sm:py-3 rounded-2xl shadow text-sm sm:text-base break-words"
            :class="msg.style"
          >
            <div class="font-semibold text-xs mb-1">{{ msg.label }}</div>
            <div class="text-sm sm:text-base whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.time }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-3 sm:p-4 border-t bg-gray-50 relative">
        <!-- Overlay if not connected -->
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 z-10"
        >
          <button
            class="px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-blue-500 text-white text-base sm:text-lg font-bold shadow-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
            @click="connectAPI"
            :disabled="isConnecting"
          >
            {{ isConnecting ? "Connecting..." : "Start" }}
          </button>
        </div>

        <!-- Mode Toggle -->
        <div class="flex justify-center sm:justify-end mb-3 sm:mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-xs sm:text-sm font-medium text-gray-700">Audio</span>
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
            <span class="text-xs sm:text-sm font-medium text-gray-700">Text</span>
          </div>
        </div>

        <!-- Audio Input -->
        <div v-if="inputMode === 'audio'">
          <div class="flex flex-col sm:flex-row justify-center gap-2 sm:gap-4">
            <button
              class="px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-red-500 text-white text-base sm:text-lg font-bold shadow-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed w-full sm:w-auto"
              :disabled="!isConnected || isPlaying || isLoading"
              @click="handleToggleRecording"
            >
              {{ isRecording ? "⏹ Stop" : "🎤 Speak" }}
            </button>

            <button
              class="px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-green-600 text-white text-base sm:text-lg font-bold shadow-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed w-full sm:w-auto"
              :disabled="!chatHistory.length"
              @click="finishAndScroll"
              title="Finish & View Report"
            >
              ✓ Finish
            </button>
          </div>
        </div>

        <!-- Text Input -->
        <div v-else class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:space-x-2">
          <input
            ref="chatInput"
            v-model="userText"
            @keyup.enter="sendTextToChatbot"
            type="text"
            placeholder="Type your message..."
            class="flex-1 p-2 sm:p-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow disabled:bg-gray-100 text-sm sm:text-base"
            :disabled="!isConnected || isLoading"
          />
          <div class="flex gap-2">
            <button
              @click="sendTextToChatbot"
              :disabled="!isConnected || !userText.trim() || isLoading || isPlaying"
              class="flex-1 sm:flex-none px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-indigo-600 text-white text-sm sm:text-base font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Send
            </button>
            <button
              class="px-3 sm:px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105 text-sm sm:text-base"
              :disabled="!chatHistory.length"
              @click="showReport = true"
              title="Finish & View Report"
            >
              ✓
            </button>
          </div>
        </div>
      </div>
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
  <!-- Report Modal -->
  <ReportModal
    v-if="selectedBot"
    ref="reportModalRef"
    :show="showReport"
    :chatHistory="chatHistory"
    :userCount="userCount"
    :assistantCount="assistantCount"
    :botName="selectedBot.name"
    :userEmail="userEmail"
    :userName="userName"
    :reportGenerationInstructions="selectedBot.reportGenerationInstructions"
    :courseTitle="'Communication in Chinese Medicine Clinical Settings'"
    @close="showReport = false"
  />
  <!-- Notification -->
  <div
    v-if="notification.visible"
    class="fixed top-3 right-3 sm:top-5 sm:right-5 z-50 px-3 sm:px-4 py-2 sm:py-3 rounded-lg shadow-lg text-white text-sm sm:text-base max-w-[calc(100vw-1.5rem)]"
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
import { BASE_URL } from "@/components/base_url";
import AvatarComponent from "../components/avatar/AvatarComponent.vue";
import LeftSidebar from "../components/avatar/LeftSidebar.vue";
import ReportModal from "../components/avatar/AvatarReportModal.vue";
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
const isSidebarOpen = ref(false); // Closed by default on mobile
const inputMode = ref("audio");
const userText = ref("");
const isLoading = ref(false);
const showReport = ref(false);
const selectedProvider = ref("openrouter");
const isConnecting = ref(false);
const notification = ref({ message: "", type: "success", visible: false });
const messagesContainer = ref(null);
const showAvatar = ref(true);
const userName = ref("");
const userEmail = ref("");
const chatInput = ref(null);
const avatarAppearance = ref("");
let socket = null;
const {
  isRecording,
  isPlaying,
  avatarState,
  speakReplySequentially,
  toggleRecording,
  getAzureToken,
  avatarGender,
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
const reportModalRef = ref(null);

function finishAndScroll() {
  showReport.value = true;

  // Wait until the DOM updates and then scroll to the modal
  nextTick(() => {
    if (reportModalRef.value?.$el) {
      reportModalRef.value.$el.scrollIntoView({ 
        behavior: "smooth", 
        block: "start" 
      });
    } else {
      // Fallback: try to find the modal element
      const modalElement = document.querySelector('.bg-white.w-full.rounded-lg.shadow-xl');
      if (modalElement) {
        modalElement.scrollIntoView({ 
          behavior: "smooth", 
          block: "start" 
        });
      }
    }
  });
}
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
];
function handleUserDataUpdate({ name, email }) {
  userName.value = name;
  userEmail.value = email;
}
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
  avatarGender.value = selectedBot.value.gender || "male";
  avatarAppearance.value = selectedBot.value.appearance || "asian";
  
  // Open sidebar by default on desktop, closed on mobile
  if (window.innerWidth >= 768) {
    isSidebarOpen.value = true;
  }
  
  await getAzureToken();

});

function focusInput() {
  nextTick(() => {
    chatInput.value?.focus();
  });
}

async function sendTextToChatbot() {
  if (!isConnected.value || !userText.value.trim() || isLoading.value || isPlaying.value) return;
  await sendMessage(userText.value, "text");
  userText.value = "";
  focusInput();
}

function handleToggleRecording() {
  if (isRecording.value) {
    // stop listening explicitly
    toggleRecording.stop();
  } else {
    // start listening
    toggleRecording.start((recognizedText) => sendMessage(recognizedText, "audio"));
  }
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
      isLoading.value = true;
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
      isLoading.value = false;
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
async function connectAPI() {
  isConnecting.value = true;
  isConnected.value = false;
  try {
    let providerUrl = "/chatbot/chat_openrouter";
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
    connectWebSocket();
    if (!chatHistory.value.length && isConnected.value) {
      chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
      scrollToBottom();
    }
    await speakReplySequentially(welcomePrompt.value);
  } catch (e) {
    console.error(e);
    showNotification("❌ Failed to connect.", "error");
  } finally {
    isConnecting.value = false;
  }
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
