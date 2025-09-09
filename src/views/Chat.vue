<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <!-- Sidebar -->
    <LeftSidebar
      v-bind="{
        isOpen: isSidebarOpen,
        systemPrompt,
        welcomePrompt,
        model,
        apiKey,
        isConnected,
        tokenUsage,
        selectedProvider,
      }"
      @update:isOpen="isSidebarOpen = $event"
      @update:apiKey="apiKey = $event"
      @update:model="model = $event"
      @update:selectedProvider="selectedProvider = $event"
      @connectAPI="connectAPI"
      @clearAPI="clearAPI"
    />

    <!-- Main Chat -->
    <div class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden">
      <!-- Header -->
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">💬 Text Chat with your AI assistant</div>
        </div>
        <div class="flex gap-2">
          <button
            class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            {{ isSidebarOpen ? "⬅ Hide Left" : "➡ Show Left" }}
          </button>
          <button
            class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30"
            @click="startNewSession"
          >
            🔄 New Session
          </button>
          <button class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30" @click="goBack">
            ⬅ Back
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div
          v-for="(msg, i) in chatHistory"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-lg md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="msgClasses(msg, i)"
          >
            <div class="font-semibold text-xs mb-1">
              {{ msgSenderLabel(msg.role) }}
            </div>
            <div
              class="prose max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap"
              v-html="renderMarkdown(msg.content)"
            ></div>
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.timestamp.toLocaleTimeString() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <!-- ✨ Input Overlay Update -->
        <div
          v-if="!isConnected && selectedProvider === 'hkbu'"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key first
        </div>

        <div class="flex items-end space-x-2">
          <textarea
            ref="chatInput"
            v-model="userText"
            @keydown.enter.exact.prevent="sendTextToChatbot"
            @keydown.shift.enter.stop
            rows="1"
            placeholder="Type your message..."
            class="flex-1 p-3 rounded-2xl border border-gray-300 focus:ring-2 focus:ring-indigo-500 resize-none disabled:bg-gray-100"
            :disabled="(!isConnected && selectedProvider === 'hkbu') || isLoading"
            @input="autoResize"
          ></textarea>

          <button
            class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            @click="sendTextToChatbot"
            :disabled="
              (!isConnected && selectedProvider === 'hkbu') || !userText.trim() || isLoading
            "
          >
            Send
          </button>

          <button
            class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
            @click="showReport = true"
            :disabled="!chatHistory.length"
            title="Finish & View Report"
          >
            ✓
          </button>
        </div>
      </div>

      <!-- Report -->
      <ReportModal
        v-bind="{
          show: showReport,
          chatHistory,
          userCount,
          assistantCount,
          botName: selectedBot.name,
        }"
        @close="showReport = false"
      />
    </div>
  </div>

  <!-- Loading -->
  <div
    v-else
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 items-center justify-center"
  >
    <div class="flex items-center space-x-3">
      <svg
        class="animate-spin h-8 w-8 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span class="text-white text-2xl font-semibold">Loading Chatbot...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "../components/chatbotStore";
import { BASE_URL } from "../components/base_url";
import LeftSidebar from "../components/avatar/LeftSidebar.vue";
import ReportModal from "../components/ReportModal.vue";
import MarkdownIt from "markdown-it";
import MarkdownItKatex from "markdown-it-katex";
const markdown = new MarkdownIt();
markdown.use(MarkdownItKatex);

const props = defineProps({ botId: String });
const router = useRouter();
const chatbotStore = useChatbotStore();

const selectedBot = computed(() => chatbotStore.availableBots.find((b) => b.id === props.botId));

const chatHistory = ref([]);
const apiKey = ref("");
const systemPrompt = ref("");
const welcomePrompt = ref("");
const model = ref("");
const isConnected = ref(false);
const isSidebarOpen = ref(true);
const userText = ref("");
const isLoading = ref(false);
const showReport = ref(false);
const selectedProvider = ref("hkbu");

const chatMessages = ref(null);
const chatInput = ref(null);

function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  });
}
function focusInput() {
  nextTick(() => {
    chatInput.value?.focus();
  });
}
function renderMarkdown(text) {
  console.log(text);
  return markdown.render(text || "");
}
const assistantCount = computed(
  () => chatHistory.value.filter((m) => m.role === "assistant").length
);
const userCount = computed(() => chatHistory.value.filter((m) => m.role === "user").length);

const tokenUsage = computed(() => {
  let total = 0;
  chatHistory.value.forEach((m, i) => {
    if (m.role === "user") total += m.content?.length || 0;
    if (
      m.role === "assistant" &&
      i !== chatHistory.value.findIndex((x) => x.role === "assistant")
    ) {
      total += m.content?.length || 0;
    }
  });
  return Math.floor((total * 3) / 4);
});

onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedBot.value) return router.push("/");

  ({
    systemPrompt: systemPrompt.value,
    welcomePrompt: welcomePrompt.value,
    model: model.value,
  } = selectedBot.value);

  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true);
  }
  focusInput();
});

const goBack = () => router.push("/");

function connectAPI(auto = false) {
  // ✅ If provider is openrouter, do not check or save API key
  if (selectedProvider.value === "openrouter") {
    isConnected.value = true;
  } else {
    if (!apiKey.value && !auto) return; // only require API key for hkbu
    localStorage.setItem("chatbot_api_key", apiKey.value);
    isConnected.value = true;
  }

  // Welcome message only if chat is empty
  if (!chatHistory.value.length) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}

function clearAPI() {
  if (selectedProvider.value === "hkbu") {
    localStorage.removeItem("chatbot_api_key");
    apiKey.value = "";
  }
  isConnected.value = false;
  chatHistory.value = [];
}

function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}

async function sendTextToChatbot() {
  chatHistory.value.push(newMessage("user", userText.value));
  userText.value = "";
  scrollToBottom();
  focusInput();

  chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."));
  const idx = chatHistory.value.length - 1;
  scrollToBottom();

  isLoading.value = true;
  try {
    let providerUrl = "";
    if (selectedProvider.value == "hkbu") {
      providerUrl = `${BASE_URL}/chatbot/chat`;
    } else if (selectedProvider.value == "openrouter") {
      providerUrl = `${BASE_URL}/chatbot/chat_openrouter`;
    }
    const res = await fetch(providerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history: chatHistory.value.map(({ role, content }) => ({
          role,
          content,
        })),
        api_key: apiKey.value,
        model_name: model.value,
      }),
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    chatHistory.value[idx] = newMessage(
      "assistant",
      data?.choices?.[0]?.message?.content || data?.error || "[No response]"
    );
  } catch (e) {
    console.error(e);
    chatHistory.value[idx] = newMessage(
      "assistant",
      "❌ Sorry, an error occurred. Please try again."
    );
  } finally {
    isLoading.value = false;
    scrollToBottom();
    focusInput();
  }
}

const newMessage = (role, content) => ({
  role,
  content,
  timestamp: new Date(),
});
const msgSenderLabel = (role) => (role === "user" ? "👤 You" : "🤖 Assistant");
const msgClasses = (msg) =>
  msg.role === "user"
    ? "bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none"
    : "bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none";
</script>
