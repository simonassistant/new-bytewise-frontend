<template>
  <div class="w-full p-4 flex-1 flex flex-col">
    <!-- Main Header for All Modes -->
    <div class="text-center mb-6">
      <h1
        class="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 bg-clip-text text-transparent"
      >
        LANG 0036: AI Writing Collaboration Lab
      </h1>
      <p
        class="text-lg bg-gradient-to-r from-gray-600 via-blue-500 to-purple-500 bg-clip-text text-transparent"
      >
        Develop and demonstrate AI literacy and human-AI partnership through guided essay revision
        and assessment
      </p>
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
            :class="[
              currentMode === mode ? activeBtn : inactiveBtn,
              isThinking ? 'cursor-not-allowed opacity-50' : '',
            ]"
            :disabled="isThinking"
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
      <!-- Chatbot Section -->
      <div class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div class="w-full mx-auto flex flex-1 gap-4">
          <!-- Left: Chat messages + input -->
          <div class="flex flex-col w-1/2" style="height: 70vh">
            <!-- Message list -->
            <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
              <div
                v-for="(msg, i) in activeChatHistory"
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
              <h2 class="text-lg font-bold mb-2">
                {{ currentMode === "assessment" ? "Your Original Essay" : "Original Draft" }}
              </h2>
              <textarea
                v-model="originalDraft"
                rows="9"
                :placeholder="
                  currentMode === 'assessment'
                    ? 'Paste your original essay here...'
                    : 'Paste or write the original draft here...'
                "
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                :disabled="
                  (isOriginalDraftConfirmed && currentMode === 'assessment') ||
                  currentMode === 'training'
                "
              />
              <button
                @click="confirmDraft"
                class="w-full mt-2 px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="currentMode !== 'assessment' || isOriginalDraftConfirmed"
              >
                {{
                  currentMode === "assessment"
                    ? isOriginalDraftConfirmed
                      ? "Essay Confirmed"
                      : "Confirm Your Essay"
                    : "Modification is not allowed in Training Mode"
                }}
              </button>
            </div>

            <!-- Final Draft -->
            <div class="bg-white p-4 rounded-lg shadow">
              <h2 class="text-lg font-bold mb-2">
                {{
                  currentMode === "assessment" ? "Revised Version (Auto-Updated)" : "Final Draft"
                }}
              </h2>
              <div class="relative w-full">
                <div v-if="isUpdatingDraft" class="p-3 text-gray-500 text-sm italic">
                  Updating draft...
                </div>

                <textarea
                  v-else
                  v-model="finalDraft"
                  rows="9"
                  :placeholder="
                    currentMode === 'assessment'
                      ? 'This will be updated automatically as you revise through chat...'
                      : 'Paste or write the improved draft here...'
                  "
                  class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                  :disabled="currentMode === 'assessment' && isOriginalDraftConfirmed"
                  :readonly="currentMode === 'assessment'"
                />
              </div>
              <button
                @click="currentMode === 'assessment' ? submitAssessment() : confirmFinalDraft()"
                class="w-full mt-2 px-3 py-2 text-white rounded-lg text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                :class="currentMode === 'assessment' ? 'bg-green-600' : 'bg-blue-600'"
                :disabled="
                  (!isOriginalDraftConfirmed && currentMode === 'assessment') ||
                  isGeneratingAssessment
                "
              >
                <span v-if="isGeneratingAssessment">
                  {{
                    currentMode === "assessment"
                      ? "🔄 Generating Assessment..."
                      : "🔄 Generating Report..."
                  }}
                </span>
                <span v-else>
                  {{
                    currentMode === "assessment"
                      ? "Submit Assessment"
                      : "Confirm Final Draft & Generate Report"
                  }}
                </span>
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
  <ReportModal
    v-bind="{
      show: showReport,
      chatHistory: reportChatHistory,
      reportGenerationInstructions,
      hiddenReport,
      bccEmail,
      ccEmail,
    }"
    @close="showReport = false"
  />
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { BASE_URL } from "@/components/base_url";
import MarkdownIt from "markdown-it";
import BriefMode from "@/components/writing_bot/BriefMode.vue";
import ReportModal from "@/components/writing_bot/WritingBotReport.vue";
import { Sample_Essay } from "@/components/writing_bot/promptAndEssay.js";
import { Trainging_Mode_Prompt } from "@/components/writing_bot/promptAndEssay.js";
import { Assessment_Mode_Prompt } from "@/components/writing_bot/promptAndEssay.js";
import { AssessBot_Prompt } from "@/components/writing_bot/promptAndEssay.js";
import { Training_Greetings } from "@/components/writing_bot/promptAndEssay.js";
import { Assessment_Greetings } from "@/components/writing_bot/promptAndEssay.js";
// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
/* ------------ State ------------ */
const currentMode = ref("briefing");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });
const originalDraft = ref(""); // Start empty for assessment mode
const finalDraft = ref("");
const trainingChatHistory = ref([]);
const assessmentChatHistory = ref([]);
const activeChatHistory = ref([]);
const userMessage = ref("");
const chatMessages = ref(null);
const isThinking = ref(false); // ✅ new state
const showReport = ref(false);
const reportChatHistory = ref([]);
const reportGenerationInstructions = ref(
  "Please generate a short report based on the chat history and drafts provided. Remember to be short and concise."
);
const bccEmail = ref([]);
const ccEmail = ref([]);
const isGeneratingAssessment = ref(false);
const isUpdatingDraft = ref(false);
const greetings = {
  training: Training_Greetings,
  assessment: Assessment_Greetings,
  briefing: `Welcome to LANG 0036: AI Writing Collaboration Lab! Please configure your API settings to start using the system.`,
};
const hiddenReport = ref("");
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

  // Reset draft confirmation state when switching modes
  isOriginalDraftConfirmed.value = false;

  if (mode === "training") {
    // Training mode uses sample essay
    originalDraft.value = Sample_Essay;
    finalDraft.value = "";
    activeChatHistory.value = trainingChatHistory.value;
    if (trainingChatHistory.value.length === 0) {
      trainingChatHistory.value.push({
        role: "assistant",
        content: greetings.training,
        timestamp: new Date(),
      });
    }
  } else if (mode === "assessment") {
    // Assessment mode starts with empty essays (students must provide their own)
    originalDraft.value = "";
    finalDraft.value = "";
    activeChatHistory.value = assessmentChatHistory.value;
    if (assessmentChatHistory.value.length === 0) {
      assessmentChatHistory.value.push({
        role: "assistant",
        content: greetings.assessment,
        timestamp: new Date(),
      });
    }
  } else {
    activeChatHistory.value = [];
  }
  scrollToBottom();
}

async function sendMessage() {
  if (!userMessage.value.trim() || isThinking.value || !isConnected.value || !apiKey.value) return;

  activeChatHistory.value.push({
    role: "user",
    content: userMessage.value,
    timestamp: new Date(),
  });
  stats.value.exchanges++;
  userMessage.value = "";
  scrollToBottom();

  isThinking.value = true;

  try {
    // --- Build payload history separately from visible activeChatHistory ---
    let payloadHistory = [...activeChatHistory.value];

    if (currentMode.value === "assessment") {
      // Insert **system message with both drafts** only for backend
      payloadHistory = [
        {
          role: "system",
          content:
            Assessment_Mode_Prompt +
            "Original Draft:\n---\n" +
            `${originalDraft.value || "(empty)"}\n---\n\n` +
            "Current Revised Version:\n---\n" +
            `${finalDraft.value || "(empty)"}\n---\n\n` +
            "IMPORTANT: If the student makes specific edits or requests changes, provide the updated version of the essay in your response. Always include the full revised text when changes are made.",
        },
        ...payloadHistory,
      ];
    } else if (currentMode.value === "training") {
      // Insert system message for backend
      payloadHistory = [
        {
          role: "system",
          content:
            Trainging_Mode_Prompt +
            "Original Draft:\n---\n" +
            `${originalDraft.value || "(empty)"}\n---\n\n` +
            "Final Draft:\n---\n" +
            `${finalDraft.value || "(empty)"}\n---\n\n`,
        },
        ...payloadHistory,
      ];
    }
    const reply = await talkToChatbot(payloadHistory);
    if (reply) {
      activeChatHistory.value.push({ role: "assistant", content: reply, timestamp: new Date() });
      // In assessment mode, try to extract updated essay text from AI response
      scrollToBottom();
      if (currentMode.value === "assessment" && isOriginalDraftConfirmed.value) {
        await extractAndUpdateEssay();
      }
    }
  } catch {
    activeChatHistory.value.push({
      role: "assistant",
      content: "⚠️ Error connecting to server.",
      timestamp: new Date(),
    });
  } finally {
    isThinking.value = false;
  }
}

async function talkToChatbot(chat_history) {
  
  const res = await fetch(`${BASE_URL}/chatbot/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_history: chat_history,
      api_key: apiKey.value,
      model_name: model.value,
    }),
  });

  const data = await res.json();
  const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";
  return reply;
}

// Function to extract and update essay from AI response in assessment mode
async function extractAndUpdateEssay() {
  isUpdatingDraft.value = true;

  let payloadHistory = [
    {
      role: "system",
      content:
        "Extract the full revised essay from the latest assistant message. If no changes were made, reply 'no changes were made'. Always provide the complete revised text only. Do not include any explanations or additional text.\n\n" +
        "Original Draft:\n---\n" +
        `${originalDraft.value || "(empty)"}\n---\n\n` +
        "Chat History:\n" +
        activeChatHistory.value
          .map((msg) => `${msg.role === "user" ? "User" : "AI"}: ${msg.content}`)
          .join("\n"),
    },
  ];
  try {
    const reply = await talkToChatbot(payloadHistory);
    if (reply) {
      if (reply.toLowerCase().includes("no changes") && reply.trim().length < 25) {
        // No update to final draft
        return;
      }
      finalDraft.value = reply.trim();
    }
  } catch (error) {
    console.error("Error extracting essay:", error);
  } finally {
    isUpdatingDraft.value = false;
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
    // ✅ check if provider replied with content
    const reply = await talkToChatbot([
      { role: "system", content: "connection test, return 1 if you can read the text." },
      { role: "user", content: "Hello!" },
    ]);

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
  activeChatHistory.value = [];
}

function showNotification(msg, type = "success") {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
}

function confirmDraft() {
  if (originalDraft.value.trim()) {
    isOriginalDraftConfirmed.value = true;

    if (currentMode.value === "assessment") {
      // In assessment mode, copy original to final draft to start revision process
      finalDraft.value = originalDraft.value;
    } else {
      // In training mode, copy to final draft for manual editing
      finalDraft.value = originalDraft.value;
    }
  } else {
    alert(
      currentMode.value === "assessment"
        ? "Please paste your original essay first."
        : "Please paste the original draft first."
    );
  }
}

async function generateAssessmentReport(mode = "final") {
  isGeneratingAssessment.value = true;
  try {
    const assessmentData = {
      originalEssay: originalDraft.value,
      revisedEssay: finalDraft.value,
      chatHistory: activeChatHistory.value.map((msg) => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
      })),
    };

    const assessmentSystemMessage = {
      role: "system",
      content:
        AssessBot_Prompt +
        "\n\nOriginal Essay:\n---\n" +
        assessmentData.originalEssay +
        "\n---\n\nRevised Essay:\n---\n" +
        assessmentData.revisedEssay +
        "\n---\n\nChat History:\n" +
        JSON.stringify(assessmentData.chatHistory, null, 2),
    };

    const userPrompt =
      mode === "training"
        ? "Please provide a comprehensive assessment report for this student's training performance based on the provided original essay, revised essay, and chat history. Focus on both essay improvement and demonstration of AI collaboration skills during training."
        : "Please provide a comprehensive assessment report for this student's performance based on the provided original essay, revised essay, and chat history. Follow the structured format specified in your system prompt.";

    const assessmentReport = await talkToChatbot([
      assessmentSystemMessage,
      { role: "user", content: userPrompt },
    ]);

    // Report template depends on mode
    reportGenerationInstructions.value =
      mode === "training"
        ? `TRAINING MODE ASSESSMENT REPORT

          Generated by AssessBot for training completion:

          ${assessmentReport}

          This report shows the student's progress in learning AI collaboration skills and essay revision during training mode.`
        : `COMPREHENSIVE STUDENT ASSESSMENT REPORT

          Generated by AssessBot using dual rubric assessment:

          ${assessmentReport}

          This report evaluates both essay writing improvement and human-AI collaboration skills according to LANG 0036 course rubrics.`;

    bccEmail.value = ["simonwanghkteacher@gmail.com"];
    hiddenReport.value = assessmentReport;
    reportChatHistory.value = [
      {
        role: "system",
        content:
          "Original Essay:\n---\n" +
          `${originalDraft.value || "(empty)"}\n---\n\n` +
          "Revised Essay:\n---\n" +
          `${finalDraft.value || "(empty)"}\n---\n\n`,
        timestamp: new Date(),
      },
      ...activeChatHistory.value,
    ];

    showReport.value = true;
    showNotification(
      mode === "training"
        ? "📊 Training assessment report generated!"
        : "📊 Assessment report generated successfully!",
      "success"
    );
  } catch (error) {
    console.error("Error generating assessment report:", error);
    showNotification("⚠️ Error generating assessment report. Using fallback.", "error");

    // Fallback report
    bccEmail.value = ["simonwanghkteacher@gmail.com"];
    reportChatHistory.value = [
      {
        role: "system",
        content:
          "Original Draft:\n---\n" +
          `${originalDraft.value || "(empty)"}\n---\n\n` +
          "Final Draft:\n---\n" +
          `${finalDraft.value || "(empty)"}\n---\n\n`,
        timestamp: new Date(),
      },
      ...activeChatHistory.value,
    ];
    showReport.value = true;
  } finally {
    isGeneratingAssessment.value = false;
  }
}

// Refined submitAssessment
async function submitAssessment() {
  if (isOriginalDraftConfirmed.value && originalDraft.value.trim()) {
    userMessage.value = "done";
    await sendMessage();
    setTimeout(() => generateAssessmentReport("final"), 1000);
  } else {
    alert("Please confirm your original essay first.");
  }
}

// Refined confirmFinalDraft
async function confirmFinalDraft() {
  if (originalDraft.value.trim() && finalDraft.value.trim()) {
    await generateAssessmentReport("training");
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
