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
          <p class="text-xs text-gray-600 mt-1">
            Or enter class access code: <span class="font-mono">aichangestheworld</span>
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
              :disabled="!apiKey"
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

        <!-- Context Window Indicator -->
        <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <h3 class="font-semibold text-orange-800 mb-3">
            🪟 Context Window
          </h3>
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Current Usage:</span>
              <span class="font-mono font-semibold text-orange-700">
                {{ formatNumber(calculateContextUsage()) }}
              </span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Model Limit:</span>
              <span class="font-mono text-gray-500">
                {{ formatNumber(getCurrentContextLimit()) }}
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-1.5 mt-2">
              <div 
                class="h-1.5 rounded-full transition-all duration-300"
                :class="getContextUsagePercentage() > 80 ? 'bg-red-500' : getContextUsagePercentage() > 60 ? 'bg-yellow-500' : 'bg-green-500'"
                :style="{ width: getContextUsagePercentage() + '%' }"
              ></div>
            </div>
            <div class="text-xs text-gray-500 text-center">
              Model: {{ displayModelName }} • Context resets when conversation is too long
            </div>
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
      <!-- Chat Messages with simple message bubbles -->
      <div class="chat-messages flex-1 overflow-y-auto p-5" ref="chatContainer">
        <!-- Simple message display replacing ChatBubble -->
        <div
          v-for="(msg, i) in displayedMessages"
          :key="i"
          :class="['message-bubble mb-4 flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
        >
          <div
            :class="[
              'max-w-[75%] p-3 rounded-lg shadow',
              msg.role === 'user' 
                ? 'bg-indigo-500 text-white rounded-br-sm' 
                : 'bg-white border rounded-bl-sm'
            ]"
          >
            <div class="text-sm mb-1 opacity-75">
              {{ msg.role === 'user' ? 'You' : selectedBot.name }}
            </div>
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs mt-2 opacity-60">
              {{ msg.timestamp.toLocaleTimeString() }}
            </div>
          </div>
        </div>
        <!-- Typing indicator (if assistant is responding) -->
        <div v-if="isLoading" class="typing-indicator">
          <div class="typing-bubble">
            <div class="ai-avatar">🤖</div>
            <div class="typing-animation">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key or class access code first
        </div>
        <!-- Lightweight state debug indicator -->
        <div class="absolute left-4 -top-3 text-[10px] px-2 py-0.5 rounded bg-indigo-600 text-white shadow">
          Mode: {{ conversationState.mode }} • Step: {{ conversationState.step }}<span v-if="conversationState.topic"> • Topic: {{ conversationState.topic }}</span>
        </div>

        <!-- Text Input (always typing mode) -->
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

// Computed property for user-friendly model display
const displayModelName = computed(() => {
  const modelName = model.value || 'google/gemini-flash-1.5';
  console.log('🎯 displayModelName computed - raw model.value:', model.value, 'fallback modelName:', modelName);
  const friendlyNames = {
    'google/gemini-flash-1.5': 'Google Gemini Flash 1.5',
    'anthropic/claude-3-sonnet': 'Claude 3 Sonnet',
    'meta-llama/llama-2-70b-chat': 'Llama 2 70B',
    'gpt-4': 'GPT-4',
    'gpt-4-turbo': 'GPT-4 Turbo'
  };
  const result = friendlyNames[modelName] || modelName;
  console.log('🎯 Final display name result:', result);
  return result;
});

const chatHistory = ref([]);
const MAX_RENDERED_MESSAGES = 200; // limit DOM nodes for memory optimization
const MAX_STORED_MESSAGES = 1000; // hard cap to prevent unbounded growth
const displayedMessages = computed(() => {
  if (!chatHistory.value || chatHistory.value.length <= MAX_RENDERED_MESSAGES) return chatHistory.value;
  return chatHistory.value.slice(-MAX_RENDERED_MESSAGES);
});
const notifications = ref([]);
const apiKey = ref("");
const CLASS_CODE_STORAGE_KEY = 'chatbot_class_code';
const classCode = ref("");
const systemPrompt = ref('');
const welcomePrompt = ref('');
const model = ref('');
const isConnected = ref(false);
const messageInput = ref("");
const showReport = ref(false);
const isSidebarOpen = ref(true);

// Sprint 1: Data properties for input mode (text-based only)
const isLoading = ref(false);
const chatContainer = ref(null);
const textareaRef = ref(null);

// Token counter variables
const sessionTokens = ref(0);

// Context window limits for different models
const CONTEXT_LIMITS = {
  'gpt-4': 8192,
  'gpt-4-turbo': 128000,
  'gpt-3.5-turbo': 16384,
  'google/gemini-flash-1.5': 32000,
  'anthropic/claude-3-sonnet': 200000,
  'meta-llama/llama-2-70b-chat': 4096,
  'default': 32000  // Default to Gemini Flash 1.5 context window
};

// Add conversation state management
const conversationState = ref({
  mode: 'welcome', // welcome, menu, brainstorm, review, feedback
  topic: null,
  step: 'initial', // initial, topic_selection, brainstorming, etc.
  lastValidState: null,
  // Persistent memory for outline review
  outlines: null // { one?: string, two?: string, raw: string }
});

const STORAGE_KEY = computed(() => `chatHistory_${props.botId}`);
const API_KEY_STORAGE_KEY = 'chatbot_api_key';

// UPDATED onMounted with corrected order of operations
onMounted(async () => {
  
  console.log('🚀 onMounted: Starting bot loading process...');
  
  // Clear any problematic localStorage data if needed
  if (localStorage.getItem('chatbot_api_key') === 'hkbu') {
    console.log('🧹 Clearing problematic hkbu API key from localStorage');
    localStorage.removeItem('chatbot_api_key');
  }
    
  // 1. Load bot configs FIRST, so we have the data we need.
  console.log('📦 Loading bot configs...');
  await chatbotStore.loadBots();
  console.log('📦 Available bots:', chatbotStore.availableBots.map(b => ({ id: b.id, name: b.name, model: b.model })));

  // Redirect if the bot is not valid
  if (!selectedBot.value) {
    console.log('❌ No selected bot found, redirecting to home');
    router.push('/');
    return;
  }
  
  console.log('🤖 Selected bot:', { 
    id: selectedBot.value.id, 
    name: selectedBot.value.name, 
    model: selectedBot.value.model 
  });
  
  // 2. Populate component state from the loaded bot config.
  // Now welcomePrompt.value will have the correct text.
  systemPrompt.value = selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;
  
  console.log('✅ Model set to:', model.value);
  console.log('✅ System prompt length:', systemPrompt.value?.length || 0);
  console.log('✅ Welcome prompt:', welcomePrompt.value?.substring(0, 50) + '...');

  // 3. Load saved chat history.
  const saved = localStorage.getItem(STORAGE_KEY.value);
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      chatHistory.value = parsed.map((m) => ({
        ...m,
        timestamp: new Date(m.timestamp),
      }));
  pruneHistoryIfNeeded();
    } catch (e) {
      console.error("Failed to parse chat history:", e);
    }
  }

  // 4. NOW, with all other state loaded, try to auto-connect.
  // connectAPI() will now have the correct welcomePrompt and chatHistory status.
  const savedApiKey = localStorage.getItem(API_KEY_STORAGE_KEY);
  const savedClassCode = localStorage.getItem(CLASS_CODE_STORAGE_KEY);
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true); // pass a flag to suppress "already connected" notification
  } else if (savedClassCode) {
    // Don't reveal the code; display a placeholder to indicate stored class access
    classCode.value = savedClassCode;
    apiKey.value = 'CLASS-********';
    connectAPI(true);
  }
});

function goBack() {
  router.push('/');
}

watch(
  chatHistory,
  (newHistory) => {
    if(newHistory.length > 0) {
  pruneHistoryIfNeeded();
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
  notify('DEBUG: connectAPI called', 'info');
  console.log('connectAPI called. isConnected:', isConnected.value, 'isAutoConnect:', isAutoConnect, 'apiKey:', apiKey.value, 'classCode:', classCode.value);
  if (isConnected.value && !isAutoConnect) {
    notify("Already connected!", "info");
    return;
  }

  const entered = (apiKey.value || '').trim();
  const savedClass = (classCode.value || '').trim();
  const isPlaceholder = /^CLASS-\*+$/i.test(entered);
  const isSecretCode = entered.toLowerCase() === 'aichangestheworld';
  const looksLikeClassCode = /^(?:\s*CLASS[-_:]|\s*CLASS\s+)/i.test(entered) || isSecretCode || isPlaceholder;

  // If nothing entered and no saved class, block manual connect (but allow auto-connect if saved class exists)
  if (!entered && !savedClass) {
    if (!isAutoConnect) notify("Please enter an API key or class code", "error");
    return;
  }

  if (looksLikeClassCode) {
    // If placeholder shown but we already have a saved class code, keep the saved value
    if (isPlaceholder && savedClass) {
      console.log('Using saved class code from storage during connect.');
      // Do not modify storage; just proceed
    } else {
      classCode.value = isSecretCode ? 'aichangestheworld' : entered;
      localStorage.setItem(CLASS_CODE_STORAGE_KEY, classCode.value);
    }
    // Never persist class codes into API key storage
    localStorage.removeItem(API_KEY_STORAGE_KEY);
  } else if (entered) {
    // Treat as normal API key path
    localStorage.setItem(API_KEY_STORAGE_KEY, entered);
    classCode.value = "";
    localStorage.removeItem(CLASS_CODE_STORAGE_KEY);
  } else if (savedClass) {
    // Auto-connect path: saved class exists, no apiKey entered
    console.log('Auto-connecting with saved class code.');
  }

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
  localStorage.removeItem(CLASS_CODE_STORAGE_KEY);
  
  apiKey.value = "";
  classCode.value = "";
  isConnected.value = false;
  chatHistory.value = [];
  notify("API disconnected", "info");
}

// PASTE THIS ENTIRE FUNCTION TO REPLACE YOUR OLD sendMessage

async function sendMessage() {
  console.log('🚀 sendMessage function called');
  
  if (!isConnected.value) {
    console.log('❌ Not connected - showing error');
    notify("Please connect your API key first", "error");
    return;
  }

  const message = messageInput.value.trim();
  console.log('📝 Message to send:', message);
  
  if (!message) {
    console.log('❌ Empty message - returning');
    return;
  }

  // Update conversation state based on user input
  const prevState = { ...conversationState.value };
  
  if (message.toLowerCase() === 'menu') {
    conversationState.value.mode = 'menu';
    conversationState.value.step = 'option_selection';
    conversationState.value.topic = null; // Reset topic when going back to menu
  } else if (['1', '2', '3'].includes(message)) {
    const modes = ['brainstorm', 'review', 'feedback'];
    conversationState.value.mode = modes[parseInt(message) - 1];
    conversationState.value.step = conversationState.value.mode === 'brainstorm' ? 'topic_selection' : 'initial';
    conversationState.value.topic = null; // Reset topic when selecting new mode
  } else if (conversationState.value.mode === 'brainstorm' && conversationState.value.step === 'topic_selection') {
    conversationState.value.topic = message;
    conversationState.value.step = 'brainstorming';
  } else if (conversationState.value.mode === 'brainstorm' && conversationState.value.step === 'brainstorming') {
    // We're already in brainstorming mode with a topic - keep the context
    // Don't change the state, just continue the conversation
  }

  // Heuristic: If user pasted outlines while not explicitly in review, switch to review and capture them
  const outlineHeuristic = message.length > 120 || /\b(introduction|body|conclusion|thesis|outline|outline\s*1|outline\s*2|^1[).:-]|^2[).:-])\b/i.test(message);
  if (outlineHeuristic && conversationState.value.mode !== 'review') {
    conversationState.value.mode = 'review';
    conversationState.value.step = 'outlines_received';
    conversationState.value.outlines = extractOutlinesFromMessage(message);
  }

  // Store last valid state
  conversationState.value.lastValidState = prevState;
  
  // Enhanced message preparation with more context across modes
  let messageToSend = message;
  
  // If we're in brainstorming mode with a topic, provide comprehensive context
  if (conversationState.value.mode === 'brainstorm' && 
      conversationState.value.step === 'brainstorming' && 
      conversationState.value.topic) {
    
    // Get recent conversation for context
    const recentExchange = chatHistory.value.slice(-4, -1).map(m => 
      `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`
    ).join(' | ');
    
    messageToSend = `[BRAINSTORMING SESSION - Topic: "${conversationState.value.topic}" | Recent context: ${recentExchange}] User says: ${message}`;
  }
  
  // Enhanced system prompt with comprehensive context for ALL modes
  let augmentedSystemPrompt = systemPrompt.value;
  const recentMessages = chatHistory.value.slice(-6).map(m => `${m.role}: ${m.content}`).join('\n');
  const baseContext = `
CURRENT MODE: ${conversationState.value.mode}
CURRENT STEP: ${conversationState.value.step}${conversationState.value.topic ? `\nCURRENT TOPIC: ${conversationState.value.topic}` : ''}
RULES:
`; 

  if (conversationState.value.mode === 'brainstorm' && conversationState.value.step === 'brainstorming' && conversationState.value.topic) {
    augmentedSystemPrompt = `${systemPrompt.value}
${baseContext}
ROLE: Creative Partner (Protocol 1: Brainstorm ideas)
OBJECTIVE: Guide the student from topic to arguable thesis with Socratic questions.

RECENT CONVERSATION CONTEXT:\n${recentMessages}
Remember: Stay focused on brainstorming about "${conversationState.value.topic}" and build upon prior turns.`;
  } else if (conversationState.value.mode === 'review') {
    augmentedSystemPrompt = `${systemPrompt.value}
${baseContext}
ROLE: Architect (Protocol 2: Review an essay outline)
OBJECTIVE: Check structure, flow, and thesis support. Ask targeted questions.

RECENT CONVERSATION CONTEXT:\n${recentMessages}`;
    // If outlines are provided now (heuristic), capture and persist them
    const looksLikeOutline = message.length > 120 || /\b(introduction|body|conclusion|thesis|outline|outline\s*1|outline\s*2|^1[).:-]|^2[).:-])\b/i.test(message);
    if (looksLikeOutline) {
      const parsed = extractOutlinesFromMessage(message);
      conversationState.value.outlines = parsed;
      // Mark step for review flow
      conversationState.value.step = 'outlines_received';
      messageToSend = `[OUTLINE REVIEW SESSION] Outline(s) provided. Please analyze the following outlines and then respond to the user query. USER QUERY: ${summarizeForInline(message)} \n\nOUTLINES RAW:\n${trimForContext(parsed.raw, 3000)}${parsed.one || parsed.two ? `\n\nOUTLINE 1:\n${trimForContext(parsed.one || '', 1500)}\n\nOUTLINE 2:\n${trimForContext(parsed.two || '', 1500)}` : ''}`;
    } else {
      messageToSend = `[OUTLINE REVIEW SESSION] User says: ${message}`;
    }

    // Always inject persistent outline context if available
    if (conversationState.value.outlines && conversationState.value.outlines.raw) {
      const o = conversationState.value.outlines;
      const persistent = `\n\nPERSISTENT OUTLINE CONTEXT (carry across turns):\n- If relevant, base your reasoning on the student-provided outlines below.\n- Do NOT ask the user to resend them; you already have them.\n\nRAW OUTLINES (truncated):\n${trimForContext(o.raw, 2500)}${o.one || o.two ? `\n\nOUTLINE 1 (truncated):\n${trimForContext(o.one || '', 1200)}\n\nOUTLINE 2 (truncated):\n${trimForContext(o.two || '', 1200)}` : ''}\n`;
      augmentedSystemPrompt += persistent;
    }
  } else if (conversationState.value.mode === 'feedback') {
    augmentedSystemPrompt = `${systemPrompt.value}
${baseContext}
ROLE: Examiner (Protocol 3: Provide feedback on an essay)
OBJECTIVE: Guide through IELTS criteria systematically, starting with Task Achievement.

RECENT CONVERSATION CONTEXT:\n${recentMessages}`;
    if (message.length > 200) {
      messageToSend = `[ESSAY FEEDBACK SESSION] Essay/Excerpt provided: ${message}`;
    } else {
      messageToSend = `[ESSAY FEEDBACK SESSION] User says: ${message}`;
    }
  }

  // Always inject persistent outlines if present (helps follow-up turns like "how to revise" reference the same outlines)
  if (conversationState.value.outlines && conversationState.value.outlines.raw) {
    const o = conversationState.value.outlines;
    const persistent = `\n\nPERSISTENT OUTLINE CONTEXT (carry across turns):\n- Base your reasoning on the stored outlines when relevant.\n- Do NOT ask the user to resend them; they are provided below.\n\nRAW OUTLINES (truncated):\n${trimForContext(o.raw, 2500)}${o.one || o.two ? `\n\nOUTLINE 1 (truncated):\n${trimForContext(o.one || '', 1200)}\n\nOUTLINE 2 (truncated):\n${trimForContext(o.two || '', 1200)}` : ''}\n`;
    augmentedSystemPrompt += persistent;
  }

  chatHistory.value.push({
    role: "user",
    content: message,
    timestamp: new Date(),
  });

  // Debug: Print chat history after user message
  console.log('Current chat history after user message:', JSON.stringify(chatHistory.value, null, 2));

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

  console.log('🌐 About to make API call to:', "https://smartlessons-production.up.railway.app/api/chat");
  console.log('📤 API payload:', {
    message: messageToSend,
  apiKey: apiKey.value ? (classCode.value ? '[CLASS_CODE]' : '[HIDDEN]') : 'MISSING',
  classCode: classCode.value ? '[SET]' : undefined,
    provider: "hkbu",
    model: model.value,
    systemPrompt: augmentedSystemPrompt ? '[SET]' : 'MISSING',
    conversationContext: {
      mode: conversationState.value.mode,
      step: conversationState.value.step,
      topic: conversationState.value.topic,
      messageCount: chatHistory.value.length
    }
  });

  try {
    const response = await fetch(
      "https://smartlessons-production.up.railway.app/api/chat",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: messageToSend,
          apiKey: classCode.value ? undefined : apiKey.value,
          classCode: classCode.value || undefined,
          provider: "hkbu",
          model: model.value,
          systemPrompt: augmentedSystemPrompt,
          conversationContext: {
            mode: conversationState.value.mode,
            step: conversationState.value.step,
            topic: conversationState.value.topic,
            messageCount: chatHistory.value.length
          }
        }),
      }
    );

    console.log('📡 API response status:', response.status);
    console.log('📡 API response OK:', response.ok);

    // Remove the "typing..." message from the UI
    chatHistory.value = chatHistory.value.filter((m) => !m.typing);
    
    // Check for network or server errors first
    if (!response.ok) {
        console.log('❌ API response not OK, trying to parse error');
        const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response.' }));
        console.log('❌ Error data:', errorData);
        throw new Error(errorData.error || `Request failed with status ${response.status}`);
    }

    console.log('✅ API response OK, parsing JSON...');
    const data = await response.json();

    // Debug: Log the full response to see token structure
    console.log('=== API RESPONSE DEBUG ===');
    console.log('Full API Response:', JSON.stringify(data, null, 2));
    console.log('Response has "usage" field:', !!data.usage);
    console.log('Response has "tokenUsage" field:', !!data.tokenUsage);
    console.log('Response has "tokens" field:', !!data.tokens);
    console.log('Response keys:', Object.keys(data));
    
    if (data.usage) {
      console.log('Usage object:', JSON.stringify(data.usage, null, 2));
    }

    if (data.response) {
      chatHistory.value.push({
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      });

      // Debug: Print chat history after assistant response
      console.log('Current chat history after assistant response:', JSON.stringify(chatHistory.value, null, 2));
      
      // Extract and update token usage - try multiple possible fields
      let tokensUsed = 0;
      if (data.usage && data.usage.total_tokens) {
        tokensUsed = data.usage.total_tokens;
        console.log('✅ Found tokens in data.usage.total_tokens:', tokensUsed);
      } else if (data.usage && data.usage.totalTokens) {
        tokensUsed = data.usage.totalTokens;
        console.log('✅ Found tokens in data.usage.totalTokens:', tokensUsed);
      } else if (data.tokenUsage) {
        tokensUsed = data.tokenUsage;
        console.log('✅ Found tokens in data.tokenUsage:', tokensUsed);
      } else if (data.tokens) {
        tokensUsed = data.tokens;
        console.log('✅ Found tokens in data.tokens:', tokensUsed);
      } else if (data.usage && data.usage.prompt_tokens && data.usage.completion_tokens) {
        tokensUsed = data.usage.prompt_tokens + data.usage.completion_tokens;
        console.log('✅ Calculated tokens from prompt + completion:', tokensUsed);
      } else {
        console.log('❌ No token data found in any expected field');
        // Fallback: Estimate tokens based on message length
        const messageLength = message.length;
        const responseLength = data.response.length;
        // Rough estimate: ~4 characters per token for English text
        tokensUsed = Math.ceil((messageLength + responseLength) / 4);
        console.log('📊 Estimated tokens based on text length:', tokensUsed);
        console.log('📝 Input length:', messageLength, 'Response length:', responseLength);
        
        // Also log to terminal via fetch to our local logging endpoint
        fetch('/api/log', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            level: 'info',
            message: `TOKEN COUNTER: Estimated ${tokensUsed} tokens for message exchange (${messageLength} + ${responseLength} chars)`,
            timestamp: new Date().toISOString()
          })
        }).catch(() => {}); // Silently fail if logging endpoint doesn't exist
      }
      
      console.log('Final tokens to add:', tokensUsed);
      console.log('Current session tokens before update:', sessionTokens.value);
      
      if (tokensUsed > 0) {
        updateTokenCounter(tokensUsed);
        console.log('✅ Updated session tokens to:', sessionTokens.value);
      } else {
        console.log('❌ No tokens to update (tokensUsed = 0)');
      }
      
      console.log('=== END DEBUG ===');
    } else {
      throw new Error(data.error || "Received an empty response from the server.");
    }
  } catch (error) {
    console.log('💥 Error caught in sendMessage:', error);
    console.log('💥 Error message:', error.message);
    console.log('💥 Error stack:', error.stack);
    
    // Make sure typing indicator is removed even if there's an error
    chatHistory.value = chatHistory.value.filter((m) => !m.typing);
    chatHistory.value.push({
      role: "assistant",
      content: `⚠️ Error: ${error.message}`,
      timestamp: new Date(),
    });
    // Debug: Print chat history after error
    console.log('Current chat history after error:', JSON.stringify(chatHistory.value, null, 2));
  pruneHistoryIfNeeded();
  }
}

function startNewSession() {
  chatHistory.value = [];
  sessionTokens.value = 0; // Reset token counter
  
  // Clear problematic localStorage entries
  if (localStorage.getItem('chatbot_api_key') === 'hkbu') {
    localStorage.removeItem('chatbot_api_key');
    apiKey.value = "";
    isConnected.value = false;
  }
  
  // Reset conversation state
  conversationState.value = {
    mode: 'welcome',
    topic: null,
    step: 'initial',
    lastValidState: null
  };
  
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

// Token counter helper functions
function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

function updateTokenCounter(tokens) {
  console.log('updateTokenCounter called with:', tokens, 'type:', typeof tokens);
  if (typeof tokens === 'number' && tokens > 0) {
    const oldValue = sessionTokens.value;
    sessionTokens.value += tokens;
    console.log('Token counter updated:', oldValue, '->', sessionTokens.value);
    
    // Log to a global array for easy export
    if (!window.tokenLogs) window.tokenLogs = [];
    window.tokenLogs.push({
      timestamp: new Date().toISOString(),
      action: 'token_added',
      tokens: tokens,
      oldTotal: oldValue,
      newTotal: sessionTokens.value,
      model: model.value
    });
    
    // Also provide a way to download logs
    if (!window.downloadTokenLogs) {
      window.downloadTokenLogs = function() {
        const logs = JSON.stringify(window.tokenLogs, null, 2);
        const blob = new Blob([logs], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'token-logs.json';
        a.click();
        URL.revokeObjectURL(url);
      };
      console.log('📁 To download token logs, run: window.downloadTokenLogs()');
    }
  } else {
    console.log('Token counter NOT updated - invalid tokens:', tokens);
  }
}

// Context window calculation functions
function getCurrentContextLimit() {
  const currentModel = model.value || 'default';
  return CONTEXT_LIMITS[currentModel] || CONTEXT_LIMITS['default'];
}

function calculateContextUsage() {
  if (!chatHistory.value || chatHistory.value.length === 0) return 0;
  
  let totalTokens = 0;
  chatHistory.value.forEach(message => {
    // Rough estimation: 1 token ≈ 0.75 words, 1 word ≈ 5 characters
    const text = message.message || '';
    const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    totalTokens += Math.ceil(wordCount * 1.33); // Convert words to tokens
  });
  
  return totalTokens;
}

function getContextUsagePercentage() {
  const contextUsage = calculateContextUsage();
  const contextLimit = getCurrentContextLimit();
  return Math.min((contextUsage / contextLimit) * 100, 100);
}

function adjustTextareaHeight() {
    const textarea = textareaRef.value;
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
    }
}

// Prune history to avoid unbounded memory usage
function pruneHistoryIfNeeded() {
  if (!Array.isArray(chatHistory.value)) return;
  if (chatHistory.value.length > MAX_STORED_MESSAGES) {
    const excess = chatHistory.value.length - MAX_STORED_MESSAGES;
    console.log(`🧹 Pruning ${excess} old messages from chat history`);
    chatHistory.value.splice(0, excess);
  }
}

// ----------- Helpers for persistent outline memory -----------
function extractOutlinesFromMessage(text) {
  // Attempt to split into outline 1 and 2 if numbered; else keep raw
  const raw = text;
  let one = null;
  let two = null;
  // Common patterns: "1) ... 2) ...", "Outline 1: ... Outline 2: ..."
  const reNumbered = /(?:^|\n)\s*(?:outline\s*1\s*[:\-]|1[\).:\-])([\s\S]*?)(?=(?:\n\s*(?:outline\s*2\s*[:\-]|2[\).:\-]))|$)/i;
  const reSecond = /(?:^|\n)\s*(?:outline\s*2\s*[:\-]|2[\).:\-])([\s\S]*)$/i;
  const m1 = raw.match(reNumbered);
  const m2 = raw.match(reSecond);
  if (m1) one = m1[1].trim();
  if (m2) two = m2[1].trim();

  return { raw, one, two };
}

function trimForContext(text, maxLen = 1200) {
  if (!text) return '';
  if (text.length <= maxLen) return text;
  const head = Math.floor(maxLen * 0.7);
  const tail = maxLen - head - 20;
  return `${text.slice(0, head)}\n...\n${text.slice(-tail)}`;
}

function summarizeForInline(text, maxLen = 300) {
  const t = text.replace(/\s+/g, ' ').trim();
  return t.length > maxLen ? `${t.slice(0, maxLen - 3)}...` : t;
}

function scrollToBottom() {
  if (chatContainer.value) {
    setTimeout(() => {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }, 100);
  }
}

// Watch for new messages and auto-scroll
watch(chatHistory, () => {
  scrollToBottom();
}, { deep: true });
</script>

<style scoped>
/* Sprint 1: Additional styles for new components */

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: flex-end;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease-out;
}

.typing-bubble {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  border: 2px solid #e2e8f0;
  flex-shrink: 0;
}

.typing-animation {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  border-bottom-left-radius: 6px;
  padding: 12px 16px;
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-animation span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #94a3b8;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-animation span:nth-child(1) {
  animation-delay: 0ms;
}

.typing-animation span:nth-child(2) {
  animation-delay: 200ms;
}

.typing-animation span:nth-child(3) {
  animation-delay: 400ms;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  30% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Voice Recording Button */
.voice-record-btn.recording {
  animation: recordingPulse 1s infinite;
}

@keyframes recordingPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

/* Voice Input Wrapper */
.voice-input-wrapper {
  min-height: 80px;
}

/* Fade In Animation */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile Responsive Adjustments */
@media (max-width: 640px) {
  .voice-record-btn {
    padding: 12px 20px;
    font-size: 14px;
  }
  
  .voice-record-btn span:first-child {
    font-size: 18px;
  }
}
</style>