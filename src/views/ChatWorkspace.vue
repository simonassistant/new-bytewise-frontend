<template>
  <div v-if="selectedApp" class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    <div class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden">
      <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center p-3 sm:p-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white gap-2">
        <div class="flex items-center gap-3 min-w-0 flex-1">
          <button @click="goHome" class="p-2 rounded-lg bg-white/20 hover:bg-white/30">
            <span class="text-lg">←</span>
          </button>
          <div class="min-w-0">
            <h1 class="text-lg font-bold truncate">{{ selectedApp.name }}</h1>
            <div class="text-xs opacity-80">{{ currentModeLabel }}</div>
          </div>
        </div>
        <div class="flex gap-2 flex-wrap items-center">
          <div 
            class="flex items-center gap-1.5 px-2 py-1 rounded-lg text-xs"
            :class="aiStatus.connected ? 'bg-green-500/30' : 'bg-red-500/30'"
          >
            <span :class="aiStatus.connected ? 'text-green-200' : 'text-red-200'">
              {{ aiStatus.connected ? '🟢 AI Connected' : '🔴 AI Offline' }}
            </span>
            <button 
              @click="testConnection" 
              :disabled="isTesting"
              class="ml-1 px-1.5 py-0.5 bg-white/20 hover:bg-white/30 rounded text-xs"
              title="Test AI connection"
            >
              {{ isTesting ? '...' : '🔄' }}
            </button>
          </div>
          <button
            @click="showSystemPrompt = !showSystemPrompt"
            class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-sm"
          >
            📋 Prompt
          </button>
          <button
            @click="showAvatar = !showAvatar"
            class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-sm"
          >
            {{ showAvatar ? '👤 Hide Avatar' : '👤 Show Avatar' }}
          </button>
          <button
            @click="startNewSession"
            class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-sm"
          >
            🔄 New
          </button>
          <button
            v-if="chatHistory.length > 1"
            @click="showReport = true"
            class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-sm"
          >
            📊 Report
          </button>
        </div>
      </header>

      <div v-if="!aiStatus.connected" class="p-3 bg-red-50 border-b border-red-200">
        <div class="flex items-center justify-between">
          <div class="text-sm text-red-800">
            <span class="font-medium">AI not connected:</span> {{ aiStatus.error || 'API key not configured' }}
          </div>
          <button 
            @click="testConnection" 
            :disabled="isTesting"
            class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
          >
            {{ isTesting ? 'Testing...' : 'Test Connection' }}
          </button>
        </div>
      </div>

      <div v-if="showSystemPrompt" class="p-4 bg-indigo-50 border-b border-indigo-200">
        <div class="flex justify-between items-start gap-2 mb-2">
          <h3 class="font-bold text-indigo-800 text-sm">System Prompt</h3>
          <button @click="showSystemPrompt = false" class="text-indigo-600 hover:text-indigo-800 text-sm">✕</button>
        </div>
        <p class="text-sm text-indigo-900 whitespace-pre-wrap bg-white p-3 rounded-lg border border-indigo-200 max-h-48 overflow-y-auto">{{ selectedApp.systemPrompt }}</p>
      </div>

      <div v-if="showAvatar" class="flex justify-center items-center py-4 border-b bg-gray-50">
        <div class="w-32 h-32 sm:w-48 sm:h-48">
          <AvatarComponent :state="avatarState" :gender="selectedApp.gender || 'male'" :appearance="selectedApp.appearance || 'asian'" />
        </div>
      </div>

      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3">
        <div v-for="(msg, i) in chatHistory" :key="i" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div
            class="max-w-[85%] sm:max-w-2xl px-4 py-3 rounded-2xl shadow text-sm break-words"
            :class="msg.role === 'user' 
              ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none' 
              : 'bg-gray-100 border text-gray-800 rounded-bl-none'"
          >
            <div class="font-semibold text-xs mb-1 opacity-70">
              {{ msg.role === 'user' ? '👤 You' : '🤖 Assistant' }}
            </div>
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs opacity-50 mt-2 text-right">
              {{ msg.timestamp?.toLocaleTimeString() }}
            </div>
          </div>
        </div>
      </div>

      <div class="p-4 border-t bg-gray-50">
        <div class="flex justify-center mb-3">
          <div class="inline-flex items-center bg-gray-200 rounded-full p-1">
            <button
              @click="switchToTextMode"
              :class="['px-4 py-1.5 rounded-full text-sm font-medium transition', inputMode === 'text' ? 'bg-white shadow text-indigo-600' : 'text-gray-600 hover:text-gray-800']"
            >
              ⌨️ Type
            </button>
            <button
              @click="switchToVoiceMode"
              :class="['px-4 py-1.5 rounded-full text-sm font-medium transition', inputMode === 'voice' ? 'bg-white shadow text-purple-600' : 'text-gray-600 hover:text-gray-800']"
              :title="!voiceAvailable ? 'Voice requires Azure Speech credentials' : ''"
            >
              🎤 Speak
              <span v-if="!voiceAvailable" class="text-xs opacity-60">🔒</span>
            </button>
          </div>
        </div>

        <div v-if="!isConnected" class="flex items-center justify-center py-2">
          <button
            @click="connectAndStart"
            :disabled="isConnecting || !aiStatus.connected"
            class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400"
          >
            {{ isConnecting ? 'Connecting...' : !aiStatus.connected ? 'AI Offline' : '▶ Start Conversation' }}
          </button>
        </div>

        <div v-else>
          <div v-if="inputMode === 'text'" class="flex gap-2">
            <input
              ref="chatInput"
              v-model="userText"
              @keyup.enter="sendTextMessage"
              type="text"
              placeholder="Type your message..."
              :disabled="isLoading || isPlaying"
              class="flex-1 p-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100"
            />
            <button
              @click="sendTextMessage"
              :disabled="!userText.trim() || isLoading || isPlaying"
              class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold hover:bg-indigo-700 disabled:bg-gray-400"
            >
              Send
            </button>
          </div>

          <div v-else-if="inputMode === 'voice'" class="flex flex-col items-center gap-3">
            <div v-if="!voiceAvailable" class="text-center text-sm text-gray-600 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <p class="font-medium text-yellow-800">Voice mode requires Azure Speech credentials</p>
              <p class="text-xs text-yellow-700 mt-1">Please configure Azure Speech settings to use voice features</p>
            </div>
            <div v-else class="flex justify-center gap-3">
              <button
                @click="handleVoiceToggle"
                :disabled="isPlaying || isLoading"
                :class="[
                  'px-6 py-3 rounded-full font-bold shadow-lg transition',
                  isRecording ? 'bg-red-600 hover:bg-red-700 text-white animate-pulse' : 'bg-purple-600 hover:bg-purple-700 text-white',
                  (isPlaying || isLoading) && 'opacity-50 cursor-not-allowed'
                ]"
              >
                {{ isRecording ? '⏹ Stop Recording' : '🎤 Press to Speak' }}
              </button>
            </div>
          </div>

          <div v-if="isLoading" class="text-center text-sm text-gray-500 mt-2">
            {{ avatarState === 'thinking' ? '🤔 Thinking...' : avatarState === 'speaking' ? '🔊 Speaking...' : '⏳ Processing...' }}
          </div>
        </div>
      </div>
    </div>

    <ReportModal
      v-if="showReport"
      :show="showReport"
      :chatHistory="chatHistory"
      :reportGenerationInstructions="selectedApp.reportGenerationInstructions"
      :userName="userName"
      :userEmail="userEmail"
      :bccEmail="selectedApp.bccEmail"
      :ccEmail="selectedApp.ccEmail"
      :courseTitle="selectedApp.name"
      @close="showReport = false"
    />
  </div>

  <div v-else class="flex h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    <div class="text-white text-center">
      <div class="text-2xl mb-4">Loading...</div>
      <button @click="goHome" class="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30">
        ← Back to Home
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "@/components/text_chatbot/chatbotStore";
import { chatWithOpenRouter, testAIConnection } from "@/lib/chatApi";
import AvatarComponent from "@/components/avatar/AvatarComponent.vue";
import ReportModal from "@/components/avatar/AvatarReportModal.vue";
import { useAzureSpeech } from "@/components/avatar/useAzureSpeech";

const props = defineProps({ appId: { type: String, required: true } });
const router = useRouter();
const chatbotStore = useChatbotStore();

const chatHistory = ref([]);
const userText = ref("");
const isConnected = ref(false);
const isConnecting = ref(false);
const isLoading = ref(false);
const inputMode = ref("text");
const showAvatar = ref(false);
const showReport = ref(false);
const showSystemPrompt = ref(false);
const messagesContainer = ref(null);
const chatInput = ref(null);
const userName = ref("");
const userEmail = ref("");

const aiStatus = reactive({ connected: false, error: null, provider: null });
const isTesting = ref(false);

function showNotification(msg, type = "success") {
  console.log(msg);
}

const {
  isRecording,
  isPlaying,
  avatarState,
  speakReplySequentially,
  toggleRecording,
  isAzureConfigured,
} = useAzureSpeech(showNotification);

const voiceAvailable = computed(() => isAzureConfigured());

const selectedApp = computed(() => 
  chatbotStore.availableBots.find((b) => b.id === props.appId)
);

const currentModeLabel = computed(() => {
  if (inputMode.value === 'voice') {
    return voiceAvailable.value ? '🎤 Voice Mode' : '🎤 Voice Mode (Unavailable)';
  }
  return '⌨️ Text Mode';
});

const systemPrompt = computed(() => {
  if (!selectedApp.value) return "";
  return inputMode.value === "voice"
    ? "Respond in plain text only — do not use Markdown, code blocks, or bold text. Keep your reply under 2 sentences. Additionally, follow these instructions: " + selectedApp.value.systemPrompt
    : selectedApp.value.systemPrompt;
});

async function testConnection() {
  isTesting.value = true;
  try {
    const result = await testAIConnection();
    aiStatus.connected = result.connected;
    aiStatus.error = result.error || null;
    aiStatus.provider = result.provider;
  } catch (e) {
    aiStatus.connected = false;
    aiStatus.error = e.message;
  } finally {
    isTesting.value = false;
  }
}

onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedApp.value) {
    router.push("/");
    return;
  }
  await testConnection();
});

function goHome() {
  router.push("/");
}

function switchToTextMode() {
  inputMode.value = "text";
  nextTick(() => chatInput.value?.focus());
}

function switchToVoiceMode() {
  inputMode.value = "voice";
  showAvatar.value = true;
}

async function connectAndStart() {
  if (!aiStatus.connected) return;
  
  isConnecting.value = true;
  try {
    isConnected.value = true;
    if (selectedApp.value?.welcomePrompt) {
      chatHistory.value.push(newMessage("assistant", selectedApp.value.welcomePrompt));
      if (inputMode.value === "voice" && voiceAvailable.value) {
        await speakReplySequentially(selectedApp.value.welcomePrompt);
      }
    }
  } catch (e) {
    console.error(e);
  } finally {
    isConnecting.value = false;
  }
}

function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value && selectedApp.value?.welcomePrompt) {
    chatHistory.value.push(newMessage("assistant", selectedApp.value.welcomePrompt));
  }
}

async function sendTextMessage() {
  if (!userText.value.trim() || isLoading.value) return;
  await sendMessage(userText.value.trim());
  userText.value = "";
  nextTick(() => chatInput.value?.focus());
}

function handleVoiceToggle() {
  if (!voiceAvailable.value) {
    return;
  }
  if (isRecording.value) {
    toggleRecording.stop();
  } else {
    toggleRecording.start((recognizedText) => sendMessage(recognizedText));
  }
}

async function sendMessage(text) {
  if (!text.trim()) return;
  
  chatHistory.value.push(newMessage("user", text));
  chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."));
  const idx = chatHistory.value.length - 1;
  scrollToBottom();

  isLoading.value = true;
  try {
    const fullHistory = [
      { role: "system", content: systemPrompt.value },
      ...chatHistory.value.slice(0, -1).map(({ role, content }) => ({ role, content })),
    ];

    const data = await chatWithOpenRouter(fullHistory, selectedApp.value?.model || "openai/gpt-4.1-mini");
    
    let reply;
    if (data.error) {
      reply = `Error: ${data.error}`;
    } else {
      reply = data?.choices?.[0]?.message?.content || "[No response]";
    }

    chatHistory.value[idx] = newMessage("assistant", reply);
    scrollToBottom();

    if (inputMode.value === "voice" && voiceAvailable.value) {
      await speakReplySequentially(reply);
    }
  } catch (e) {
    console.error(e);
    chatHistory.value[idx] = newMessage("assistant", "Sorry, an error occurred.");
  } finally {
    isLoading.value = false;
  }
}

function newMessage(role, content) {
  return { role, content, timestamp: new Date() };
}

function scrollToBottom() {
  nextTick(() => {
    const el = messagesContainer.value;
    if (el) el.scrollTop = el.scrollHeight;
  });
}

watch(inputMode, (newMode) => {
  if (newMode === "voice") {
    showAvatar.value = true;
  }
});
</script>
