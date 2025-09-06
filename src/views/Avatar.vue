<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800 relative"
    :class="{ 'avatar-panel-open': isAvatarPanelOpen }"
  >
    <!-- Avatar Panel (overlay on right side) -->
    <AvatarPanel @panel-toggle="handleAvatarPanelToggle" />
  
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
          <p class="text-xs text-gray-600 mt-2">
            Get your key from the
            <a
              href="https://genai.hkbu.edu.hk/settings/api-docs"
              target="_blank"
              rel="noopener noreferrer"
              class="text-indigo-600 hover:underline"
            >
              HKBU Generative AI Platform </a
            >.
          </p>

          <select
            v-model="model"
            class="w-full mt-3 border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
          >
            <option value="gpt-4.1-mini">GPT-4.1 Mini</option>
            <option value="gpt-4.1">GPT-4.1</option>
            <option value="gpt-5-mini">GPT-5 Mini</option>
            <option value="gpt-o1">GPT-o1</option>
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

    <!-- Chat Area -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300"
    >
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">� Speak or type with your AI avatar • Voice responses always enabled</div>
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

      <!-- Chat history -->
      <div class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <ChatBubble
          v-for="(msg, i) in chatHistory"
          :key="i"
          :message="msg.content"
          :is-user="msg.role === 'user'"
          :timestamp="msg.timestamp"
          :avatar="msg.role === 'user' ? null : '🤖'"
        />
        
        <!-- Typing indicator -->
        <div v-if="isTyping" class="flex justify-start">
          <div class="max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none">
            <div class="font-semibold text-xs mb-1">🤖 Assistant</div>
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hybrid Input Interface - Both Voice and Typing Available -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key first
        </div>
        
        <!-- Primary Input Mode Toggle (for layout preference) -->
        <div class="mb-4">
          <InputModeToggle 
            :current-mode="inputMode" 
            @mode-changed="handleModeChange" 
          />
          <p class="text-xs text-gray-500 mt-1 text-center">💡 Voice feedback is always enabled • Switch layout preference</p>
        </div>

        <!-- Enhanced Input Interface - Shows both methods when primary mode is selected -->
        <div class="space-y-4">
          
          <!-- Voice Input Section (Always Available) -->
          <div class="voice-input-section" :class="{ 'opacity-50': inputMode === 'typing' && !isRecording }">
            <div class="flex justify-center">
              <button
                class="px-6 py-3 rounded-full bg-red-500 text-white text-lg font-bold shadow-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-200"
                :disabled="!isConnected || isPlaying || isRecognizing"
                @click="toggleRecording"
                :class="{
                  'bg-red-600 scale-105': isRecording,
                  'bg-gray-400': !isConnected || isPlaying || isRecognizing
                }"
              >
                {{ isRecording ? "⏹ Stop Recording" : "🎤 Speak" }}
              </button>
            </div>
            
            <!-- Recording Status -->
            <div v-if="isRecording" class="mt-2 text-center">
              <div class="inline-flex items-center space-x-2 text-red-600">
                <div class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                <span class="text-sm font-medium">Recording...</span>
              </div>
            </div>
          </div>

          <!-- Divider (when both are prominently shown) -->
          <div v-if="inputMode === 'hybrid'" class="flex items-center justify-center">
            <div class="flex-grow h-px bg-gray-300"></div>
            <span class="px-3 text-xs text-gray-500 bg-gray-50">OR</span>
            <div class="flex-grow h-px bg-gray-300"></div>
          </div>

          <!-- Text Input Section (Always Available) -->
          <div class="typing-input-section" :class="{ 'opacity-50': inputMode === 'voice' && !messageInput.trim() }">
            <div class="flex items-end gap-3">
              <textarea
                v-model="messageInput"
                placeholder="Type your message... (Voice feedback will still play)"
                class="flex-grow p-3 bg-gray-100 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-300 resize-none min-h-[44px] max-h-32"
                rows="1"
                ref="textareaRef"
                @input="adjustTextareaHeight"
                @keydown.enter.exact.prevent="sendTypedMessage"
              ></textarea>
              <button
                class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
                :disabled="!isConnected || !messageInput.trim()"
                @click="sendTypedMessage"
                title="Send Message (with Voice Response)"
              >
                ➤
              </button>
            </div>
          </div>
        </div>

        <!-- Audio Output (Always Available) -->
        <div class="mt-4 flex justify-center" v-if="audioUrl">
          <audio
            :src="audioUrl"
            autoplay
            @play="isPlaying = true"
            @ended="isPlaying = false"
          ></audio>
        </div>
      </div>
    </div>
  </div>

  <!-- Loading screen -->
  <div
    v-else
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 items-center justify-center"
  >
    <div class="flex items-center justify-center space-x-3">
      <svg
        class="animate-spin h-8 w-8 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      <span class="text-white text-2xl font-semibold">Loading Chatbot...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "../components/chatbotStore";
import { io } from "socket.io-client";
import { BASE_URL } from "../components/base_url";
import audioBufferToWav from "audiobuffer-to-wav";

// Import Sprint 1 components
import AvatarPanel from "../components/avatar/AvatarPanel.vue";
import ChatBubble from "../components/avatar/ChatBubble.vue";
import InputModeToggle from "../components/avatar/InputModeToggle.vue";

const props = defineProps({ avatarId: { type: String, required: true } });
const router = useRouter();
const chatbotStore = useChatbotStore();
const selectedBot = computed(() =>
  chatbotStore.availableBots.find((b) => b.id === props.avatarId)
);

const chatHistory = ref([]);
const apiKey = ref("");
const systemPrompt = ref("");
const welcomePrompt = ref("");
const model = ref("");
const isConnected = ref(false);
const isSidebarOpen = ref(true);

const isRecording = ref(false);
const isPlaying = ref(false);
const audioUrl = ref(null);
const isRecognizing = ref(false);

// Sprint 1: Input mode and UI state
const inputMode = ref(localStorage.getItem('inputMode') || 'voice');
const isTyping = ref(false);
const messageInput = ref('');
const textareaRef = ref(null);
const isAvatarPanelOpen = ref(false);

let mediaRecorder = null;
let audioChunks = [];
let socket = null;
let chunks = [];

onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedBot.value) {
    router.push("/");
    return;
  }

  systemPrompt.value = selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;

  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true);
  }
});

function goBack() {
  router.push("/");
}

function connectAPI(isAutoConnect = false) {
  if (!apiKey.value) return;
  localStorage.setItem("chatbot_api_key", apiKey.value);
  isConnected.value = true;
  if (chatHistory.value.length === 0) {
    chatHistory.value.push({
      role: "assistant",
      content: welcomePrompt.value,
      timestamp: new Date(),
    });
  }
  connectWebSocket();
}

function clearAPI() {
  localStorage.removeItem("chatbot_api_key");
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
}

function connectWebSocket() {
  socket = io(`${BASE_URL}/streaming-avatar`, { transports: ["websocket"] });

  socket.on("connect", () => {
    console.log("WS connected");
    chunks = [];
  });
  socket.on("audio_chunk", (chunk) => {
    if (chunk instanceof ArrayBuffer) chunks.push(new Uint8Array(chunk));
  });
  socket.on("audio_complete", () => {
    console.log("Audio complete, total chunks:", chunks.length);
    const blob = new Blob(chunks, { type: "audio/mpeg" });
    audioUrl.value = URL.createObjectURL(blob);
    chunks = [];
  });
  socket.on("stt_result", (result) => {
    if (result && typeof result.text === "string") {
      chatHistory.value.push({
        role: "user",
        content: result.text,
        timestamp: new Date(),
      });

      // Call Flask streaming endpoint
      sendUserMessage(result.text);
    }
    isRecognizing.value = false;
  });


  socket.on("disconnect", () => {
    console.log("WS disconnected");
  });
}

async function toggleRecording() {
  if (!isRecording.value) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
    mediaRecorder.onstop = sendAudioToBackend;
    mediaRecorder.start();
    isRecording.value = true;
  } else {
    mediaRecorder.stop();
    isRecording.value = false;
  }
}

async function sendAudioToBackend() {
  const blob = new Blob(audioChunks, { type: "audio/webm" });
  const arrayBuffer = await blob.arrayBuffer();

  // Decode WebM → AudioBuffer
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

  // Convert AudioBuffer → WAV
  const wavArrayBuffer = audioBufferToWav(audioBuffer);
  const wavBlob = new Blob([wavArrayBuffer], { type: "audio/wav" });

  if (socket && socket.connected) {
    socket.emit("user_audio", await wavBlob.arrayBuffer()); // send WAV
    isRecognizing.value = true;
  }

  // reset
  audioChunks = [];
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
}

/**
 * --- NEW: Stream assistant reply from Flask /stream_chat ---
 */
function sendUserMessage(userText) {
  if (!isConnected.value || !userText.trim() || !socket) return;
  
  // Show typing indicator
  isTyping.value = true;
  
  // Add a placeholder assistant reply while waiting
  chatHistory.value.push({
    role: "assistant",
    content: "⏳ Avatar is thinking...",
    timestamp: new Date(),
  });
  const msgIndex = chatHistory.value.length - 1;

  // Send through websocket
  socket.emit("user_message", {
    text: userText,
    system_prompt: systemPrompt.value,
    api_key: apiKey.value,
    model: model.value,
    history: chatHistory.value.map((m) => ({
      role: m.role,
      content: m.content,
    })),
  });

  // Listen for assistant reply
  socket.once("assistant_reply", (reply) => {
    isTyping.value = false;
    chatHistory.value[msgIndex] = {
      ...chatHistory.value[msgIndex],
      content: reply?.content || "[No response]",
      timestamp: new Date(),
    };
  });
}

// Sprint 1: Handle input mode changes
function handleModeChange(newMode) {
  inputMode.value = newMode;
  localStorage.setItem('inputMode', newMode);
}

// Avatar panel toggle handler
function handleAvatarPanelToggle(isOpen) {
  isAvatarPanelOpen.value = isOpen;
}

// Typing functionality
function sendTypedMessage() {
  if (!isConnected.value || !messageInput.value.trim()) return;
  
  const userMessage = messageInput.value.trim();
  
  // Add user message to history
  chatHistory.value.push({
    role: "user",
    content: userMessage,
    timestamp: new Date(),
  });
  
  // Clear input
  messageInput.value = '';
  
  // Send message using existing functionality
  sendUserMessage(userMessage);
}

function adjustTextareaHeight() {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto';
    textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 128) + 'px';
  }
}
</script>

<style scoped>
/* Adjust layout when avatar panel is open */
.avatar-panel-open {
  padding-right: 320px;
  transition: padding-right 0.3s ease;
}

/* Ensure content doesn't get covered by fixed avatar panel */
@media (max-width: 768px) {
  .avatar-panel-open {
    padding-right: 0; /* Remove padding on mobile, use overlay instead */
  }
}
</style>
