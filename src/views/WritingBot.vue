<template>
  <div class="w-full p-4 flex-1 flex flex-col">
    <!-- Header -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">EEGC Human-AI Collaboration Chatbot</h1>
      <p class="text-gray-600">Practice and assess your AI interaction skills</p>
    </div>

    <!-- Mode Selection -->
    <div class="mb-6 p-4 bg-gray-50 rounded-lg">
      <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
        <!-- Mode Buttons -->
        <div class="flex gap-4">
          <button
            v-for="mode in ['briefing', 'training', 'assessment']"
            :key="mode"
            @click="switchMode(mode)"
            :class="currentMode === mode ? activeBtn : inactiveBtn"
          >
            {{ mode.charAt(0).toUpperCase() + mode.slice(1) }} Mode
          </button>
        </div>

        <!-- Status Badge -->
        <div
          class="px-4 py-2 rounded-full text-sm font-medium"
          :class="
            {
              training: 'bg-green-100 text-green-800',
              assessment: 'bg-red-100 text-red-800',
              briefing: 'bg-blue-100 text-blue-800',
            }[currentMode]
          "
        >
          {{
            {
              training: "Training Mode Active",
              assessment: "Assessment Mode Active",
              briefing: "Briefing Mode Active",
            }[currentMode]
          }}
        </div>

        <!-- Show Skills Button -->
        <button
          v-if="['training', 'assessment'].includes(currentMode)"
          @click="showSkills = !showSkills"
          class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ showSkills ? "Hide Skills" : "Show Skills" }}
        </button>
      </div>
    </div>

    <!-- Briefing Mode Section -->
    <div v-if="currentMode === 'briefing'" class="w-full p-4 flex-1">
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <div class="text-center mb-4">
          <h2 class="text-xl font-bold text-gray-900 mb-1">Connect to Chatbot</h2>
          <p class="text-gray-600 text-sm">
            Configure your API settings to start using the chatbot
          </p>
        </div>

        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between mb-4">
          <!-- API Config -->
          <div class="flex-1 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
            <h3 class="font-semibold text-yellow-800 mb-2 text-sm">🔑 API Configuration</h3>
            <input
              type="password"
              :value="apiKey"
              @input="onApiKeyInput($event.target.value)"
              placeholder="Paste your API key..."
              class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
            />
            <p class="text-xs text-gray-600 mt-1">
              Get your key from the
              <a
                href="https://genai.hkbu.edu.hk/settings/api-docs"
                target="_blank"
                rel="noopener noreferrer"
                class="text-indigo-600 hover:underline"
                >HKBU Generative AI Platform</a
              >.
            </p>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex gap-4 justify-center">
          <button
            class="px-20 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium disabled:cursor-not-allowed transition-opacity"
            @click="connectAPI"
            :disabled="isConnecting || isConnected || !apiKey.trim()"
          >
            <span v-if="isConnecting">🔄 Connecting...</span>
            <span v-else-if="isConnected">✔️ Connected</span>
            <span v-else>✅ Connect</span>
          </button>

          <button
            class="px-20 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 text-gray-700 text-sm font-medium disabled:cursor-not-allowed transition-opacity"
            @click="clearAPI"
            :disabled="isConnecting"
          >
            🗑️ Clear
          </button>
        </div>

        <!-- Connection Status -->
        <div
          v-if="notification.visible"
          class="mt-3 p-3 rounded-lg text-sm text-center"
          :class="
            notification.type === 'success'
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          "
        >
          {{ notification.message }}
        </div>
      </div>
    </div>

    <!-- Training / Assessment Mode Section -->
    <div v-if="['training', 'assessment'].includes(currentMode)" class="flex-1 flex flex-col">
      <!-- Skills Developed -->
      <div v-if="showSkills" class="mb-4">
        <SkillesDeveloped />
      </div>

      <!-- Chatbot Section -->
      <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div class="w-full mx-auto flex flex-1 gap-4">
          <!-- Left: Chat messages + input -->
          <div class="flex flex-col w-1/2">
            <!-- Message list -->
            <div
              ref="chatMessages"
              class="chat-messages flex-1 overflow-y-auto p-5 space-y-4"
              style="max-height: 60vh;"
            >
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
                    class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
                    v-html="renderMarkdown(msg.content)"
                  />
                  <div class="text-xs text-gray-400 mt-2 text-right">
                    {{ msg.timestamp.toLocaleTimeString() }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Chat input -->
            <div class="mt-3 flex gap-2 items-end">
              <textarea
                v-model="userMessage"
                rows="3"
                :placeholder="
                  isConnected ? 'Type your message...' : 'Please connect to API first...'
                "
                class="flex-1 border rounded-lg p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                @keyup.enter.exact.prevent="sendMessage"
                :disabled="isThinking || !isConnected"
              ></textarea>
              <button
                @click="sendMessage"
                class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed h-fit"
                :disabled="isThinking || !isConnected"
              >
                {{ isThinking ? "Thinking..." : "Send" }}
              </button>
            </div>
          </div>

          <!-- Right: Draft boxes -->
          <div class="flex-1 space-y-4 overflow-y-auto h-full">
            <!-- Original Draft -->
            <div class="bg-white p-4 rounded-lg shadow">
              <h2 class="text-lg font-bold mb-2">Original Draft</h2>
              <textarea
                v-model="originalDraft"
                rows="6"
                placeholder="Paste or write the original draft here..."
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                :disabled="isOriginalDraftConfirmed"
              ></textarea>
              <button
                @click="confirmDraft"
                class="w-full mt-2 px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isOriginalDraftConfirmed"
              >
                {{ isOriginalDraftConfirmed ? "Draft Confirmed" : "Confirm Original Draft" }}
              </button>
            </div>

            <!-- Final Draft -->
            <div class="bg-white p-4 rounded-lg shadow">
              <h2 class="text-lg font-bold mb-2">Final Draft</h2>
              <textarea
                v-model="finalDraft"
                rows="6"
                placeholder="Paste or write the improved draft here..."
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                :disabled="!isOriginalDraftConfirmed"
              ></textarea>
              <button
                @click="confirmFinalDraft"
                class="w-full mt-2 px-3 py-2 bg-blue-600 text-white rounded-lg text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="!isOriginalDraftConfirmed"
              >
                Confirm Final Draft & Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Briefing Mode Content -->
    <div v-else-if="currentMode == 'briefing'" class="w-full mx-auto p-6">
      <BriefMode />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { BASE_URL } from "../components/base_url";
import MarkdownIt from "markdown-it";
import BriefMode from "@/components/writing_bot/BriefMode.vue";
import SkillesDeveloped from "@/components/writing_bot/SkillesDeveloped.vue";
import { Sample_Essay } from "@/components/writing_bot/sampleEssay.js";

// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
/* ------------ State ------------ */
const currentMode = ref("briefing");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });
const originalDraft = ref(Sample_Essay);
const finalDraft = ref("");
const showSkills = ref(true);
const chatHistory = ref([]);
const userMessage = ref("");
const chatMessages = ref(null);
const isThinking = ref(false); // ✅ new state

const greetings = {
  training: `Hello! I'm here to help you improve your essay through AI collaboration. Let's start by choosing which aspect of your essay you'd like to work on. Would you like to focus on:\n1) Content & Ideas\n2) Organisation & Structure\n3) Vocabulary\n4) Grammar & Sentence Structure`,
  assessment: `I am here to help you revise the essay. Please share an essay draft.`,
  briefing: `Welcome! Please configure your API settings to start using the chatbot.`,
};

const activeBtn =
  "px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:opacity-90 transition-opacity";
const inactiveBtn =
  "px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:opacity-90 transition-opacity";

// API Connection State
const isConnected = ref(false);
const isConnecting = ref(false);
const apiKey = ref("");
const notification = ref({ message: "", type: "success", visible: false });
const model = ref("gpt-4.1");

const sampleEssay = ref(``);

const isOriginalDraftConfirmed = ref(false);

/* ------------ Chat Helpers ------------ */
function msgSenderLabel(role) {
  return role === "user" ? "You" : "AI Assistant";
}
function msgClasses(msg) {
  return msg.role === "user"
    ? "bg-indigo-600 text-white rounded-br-none"
    : "bg-gray-100 text-gray-800 rounded-bl-none";
}

function renderMarkdown(text) {
  return markdown.render(text || "");
}

/* ------------ Methods ------------ */
function switchMode(mode) {
  currentMode.value = mode;
  stats.value = { exchanges: 0, questions: 0, revisions: 0 };
  if (chatHistory.value.length < 2)
    chatHistory.value = [{ role: "assistant", content: greetings[mode], timestamp: new Date() }];
  scrollToBottom();
}

async function sendMessage() {
  if (!userMessage.value.trim() || isThinking.value || !isConnected.value || !apiKey.value) return;

  chatHistory.value.push({
    role: "user",
    content: userMessage.value,
    timestamp: new Date(),
  });
  stats.value.exchanges++;
  userMessage.value = "";
  scrollToBottom();

  isThinking.value = true;

  try {
    // --- Build payload history separately from visible chatHistory ---
    let payloadHistory = [...chatHistory.value];

    if (currentMode.value === "assessment") {
      // Insert **system message with both drafts** only for backend
      payloadHistory = [
        {
          role: "system",
          content:
            "You are an expert writing assistant tasked with helping a student revise their own " +
            "point-of-view essay draft without any specific prompts. Engage in a detailed, " +
            "open-ended conversation to guide the student in improving their draft based on the " +
            "provided rubric (Content and Ideas, Organisation and Logical Progression, Vocabulary, " +
            "Grammar and Sentence Structure). Offer tailored feedback to enhance the essay’s relevance, " +
            "clarity, depth, logical flow, vocabulary, and grammar. Ask insightful, multi-level questions " +
            "to encourage critical thinking and help the student evaluate their work. Support an iterative " +
            "revision process by suggesting specific improvements and encouraging the student to justify their " +
            "choices. Ensure all exchanges are well-documented, showcasing the depth of the conversation and the student’s " +
            "critical engagement with your suggestions.\n" +
            "Here are the drafts:\n" +
            "Original Draft:\n---\n" +
            `${originalDraft.value || "(empty)"}\n---\n\n` +
            "Final Draft:\n---\n" +
            `${finalDraft.value || "(empty)"}\n---\n\n`,
        },
        ...payloadHistory,
      ];
    } else if (currentMode.value === "training") {
      // Insert system message  for backend
      payloadHistory = [
        {
          role: "system",
          content:
            "You are an expert writing assistant designed to help students revise" +
            "a teacher-provided draft to improve its quality as a point-of-view essay. " +
            "Your role is to engage in an in-depth conversation with the student, providing " +
            "clear, constructive feedback based on the provided rubric (Content and Ideas, " +
            "Organisation and Logical Progression, Vocabulary, Grammar and Sentence Structure). " +
            "Offer specific suggestions to enhance the draft’s relevance, clarity, depth, organisation, " +
            "vocabulary, and grammar. Ask targeted questions to guide the student in critically evaluating " +
            "the draft and encourage them to justify their revision choices. Provide appropriate prompts to " +
            "ensure the conversation remains focused and productive, fostering a robust iterative revision process. " +
            "Document all exchanges clearly to reflect the depth of the conversation and the student’s engagement.\n" +
            "Teacher-provided Draft:\n---\n" +
            `${sampleEssay.value}`,
        },
        ...payloadHistory,
      ];
    }

    //using openrouter chatbot
    // const res = await fetch(`${BASE_URL}/chatbot/chat`, {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ chat_history: payloadHistory }),
    // });
    // using hkbu chatbot
    const res = await fetch(`${BASE_URL}/chatbot/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history: payloadHistory,
        api_key: apiKey.value,
        model_name: model.value,
      }),
    });

    const data = await res.json();
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";

    if (reply) {
      chatHistory.value.push({ role: "assistant", content: reply, timestamp: new Date() });
      scrollToBottom();
    }
  } catch {
    chatHistory.value.push({
      role: "assistant",
      content: "⚠️ Error connecting to server.",
      timestamp: new Date(),
    });
  } finally {
    isThinking.value = false;
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  });
}

// API Key Input Handler
function onApiKeyInput(value) {
  apiKey.value = value;
}

async function connectAPI(auto = false) {
  if (!apiKey.value && !auto) return;
  localStorage.setItem("chatbot_api_key", apiKey.value);

  isConnecting.value = true;
  // 🔍 test provider connection by sending a dummy message
  try {
    const providerUrl = `${BASE_URL}/chatbot/chat`;

    const res = await fetch(providerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history: [
          { role: "system", content: "connection test, return 1 if you can read the text." },
          { role: "user", content: "Hello!" },
        ],
        api_key: apiKey.value,
        model_name: model.value,
      }),
    });

    const data = await res.json();

    // ✅ check if provider replied with content
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";

    if (reply && reply.trim().length > 0) {
      showNotification("✅ Connected and working!", "success");
      isConnected.value = true;
      // Auto-switch to training mode after successful connection
      if (currentMode.value === "briefing") {
        switchMode("training");
      }
    } else {
      showNotification("⚠️ Connected, but no valid reply received.", "error");
      isConnected.value = false;
    }
  } catch (err) {
    console.error(err);
    showNotification("❌ Failed to connect.", "error");
    isConnected.value = false;
  } finally {
    isConnecting.value = false;
  }
}

function clearAPI() {
  localStorage.removeItem("chatbot_api_key");
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
}

function showNotification(msg, type = "success") {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
}

function confirmDraft() {
  if (originalDraft.value.trim()) {
    isOriginalDraftConfirmed.value = true;
    finalDraft.value = originalDraft.value;
  } else {
    alert("Please paste the original draft first.");
  }
}

function confirmFinalDraft() {
  if (isOriginalDraftConfirmed.value && originalDraft.value.trim() && finalDraft.value.trim()) {
    alert("Report generated.");
  } else {
    alert("Please paste the final draft first.");
  }
}

onMounted(async () => {
  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    await connectAPI(true);
  }
  // ✅ Auto-init
  switchMode(currentMode.value);
});
</script>
