<template>
  <div class="w-full p-4 flex-1 flex flex-col">
    <!-- Header -->
    <div class="text-center mb-6">
      <p
        class="text-3xl font-bold mb-4 leading-normal bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 bg-clip-text text-transparent"
      >
        LANG 0036: AI Writing Collaboration Lab
      </p>
      <p
        class="text-xl font-bold mb-4 leading-normal bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 bg-clip-text text-transparent"
      >
        Remember to submit your chat history by clicking on (green mark)~
      </p>
      <p
        class="text-lg leading-normal bg-gradient-to-r from-gray-600 via-blue-500 to-purple-500 bg-clip-text text-transparent"
      >
        Develop and demonstrate AI literacy and human-AI partnership through guided essay revision
        and assessment
      </p>
    </div>

    <!-- Mode Selection -->
    <div class="mb-6 p-4 bg-gray-50 rounded-lg">
      <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
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

        <div class="px-4 py-2 rounded-full text-sm font-medium" :class="modeColors[currentMode]">
          {{ modeLabels[currentMode] }}
        </div>
      </div>
    </div>

    <!-- Mode Rendering -->
    <template v-if="currentMode === 'briefing'">
      <div class="w-full p-4 flex-1">
        <div class="mb-6 p-4 bg-gray-50 rounded-lg text-center">
          <h2 class="text-xl font-bold text-gray-900 mb-1">Connect to Chatbot</h2>
          <p class="text-gray-600 text-sm mb-4">
            Configure your API settings to start using the chatbot
          </p>

          <div class="flex flex-col gap-4 justify-center items-stretch w-full">
            <div class="w-full bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 class="font-semibold text-yellow-800 mb-2 text-sm">🔑 API Configuration</h3>
              <input
                type="password"
                v-model="apiKey"
                placeholder="Paste your API key..."
                class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
              />
              <p class="text-xs text-gray-600 mt-1">
                Get your key from
                <a
                  href="https://genai.hkbu.edu.hk/settings/api-docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-indigo-600 hover:underline"
                >
                  HKBU Generative AI Platform </a
                >.
              </p>
            </div>
          </div>

          <div class="flex gap-4 justify-center mt-4">
            <button
              class="px-20 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium disabled:opacity-50 transition-opacity"
              @click="connectAPI"
              :disabled="isConnecting || isConnected || !apiKey.trim()"
            >
              <span v-if="isConnecting">🔄 Connecting...</span>
              <span v-else-if="isConnected">✔️ Connected</span>
              <span v-else>✅ Connect</span>
            </button>
            <button
              class="px-20 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 text-gray-700 text-sm font-medium"
              @click="clearAPI"
              :disabled="isConnecting"
            >
              🗑️ Clear
            </button>
          </div>

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
      <BriefMode />
    </template>

    <!-- Chat Interface -->
    <ChatInterface
      v-else
      v-model:userMessage="userMessage"
      v-model:originalDraft="originalDraft"
      v-model:finalDraft="finalDraft"
      :activeChatHistory="activeChatHistory"
      :currentMode="currentMode"
      :isConnected="isConnected"
      :isThinking="isThinking"
      :isUpdatingDraft="isUpdatingDraft"
      :isGeneratingAssessment="isGeneratingAssessment"
      :isOriginalDraftConfirmed="isOriginalDraftConfirmed"
      :isSubmitted="isSubmitted"
      @sendMessage="sendMessage"
      @confirmDraft="confirmDraft"
      @submitAssessment="submitAssessment"
      @confirmFinalDraft="confirmFinalDraft"
    />

    <!-- Report Modal -->
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
      @submit="isSubmitted = true"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import BriefMode from "@/components/writing_bot/BriefMode.vue";
import ReportModal from "@/components/writing_bot/WritingBotReport.vue";
import ChatInterface from "@/components/writing_bot/ChatInterface.vue";
import { useChatFunctions } from "@/components/writing_bot/useChatFunctions";
import {
  Sample_Essay,
  AssessBot_Prompt,
  Training_Greetings,
  Assessment_Greetings,
} from "@/components/writing_bot/promptAndEssay.js";

/* ------------ State ------------ */
const currentMode = ref("briefing");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });

/* Separate drafts by mode */
const trainingOriginalDraft = ref("");
const trainingFinalDraft = ref("");
const assessmentOriginalDraft = ref("");
const assessmentFinalDraft = ref("");

/* Active working drafts */
const originalDraft = ref("");
const finalDraft = ref("");
const userMessage = ref("");

/* Chat histories per mode */
const trainingChatHistory = ref([]);
const assessmentChatHistory = ref([]);
const activeChatHistory = ref([]);

/* Other UI and session states */
const showReport = ref(false);
const reportChatHistory = ref([]);
const reportGenerationInstructions = ref("");
const isSubmitted = ref(false);
const bccEmail = ref([]);
const ccEmail = ref([]);
const isGeneratingAssessment = ref(false);
const isUpdatingDraft = ref(false);
const hiddenReport = ref("");
const apiKey = ref("");
const notification = ref({ message: "", type: "success", visible: false });
const isThinking = ref(false);
const isConnected = ref(false);
const isConnecting = ref(false);
const model = ref("gpt-4.1");
const isOriginalDraftConfirmed = ref(false);

const activeBtn = "px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold";
const inactiveBtn = "px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-semibold";

const modeColors = {
  training: "bg-green-100 text-green-800",
  assessment: "bg-red-100 text-red-800",
  briefing: "bg-blue-100 text-blue-800",
};

const modeLabels = {
  training: "Training Mode Active",
  assessment: "Assessment Mode Active",
  briefing: "Briefing Mode Active",
};

const greetings = {
  training: Training_Greetings,
  assessment: Assessment_Greetings,
  briefing: "Welcome to LANG 0036! Configure your API to start.",
};

const { sendMessage, talkToChatbot } = useChatFunctions({
  userMessage,
  currentMode,
  activeChatHistory,
  originalDraft,
  finalDraft,
  isConnected,
  apiKey,
  model,
  isThinking,
  isOriginalDraftConfirmed,
  isUpdatingDraft,
});

/* ------------ Mode Switching ------------ */
function switchMode(mode) {
  // Save current drafts before switching
  if (currentMode.value === "training") {
    trainingOriginalDraft.value = originalDraft.value;
    trainingFinalDraft.value = finalDraft.value;
  } else if (currentMode.value === "assessment") {
    assessmentOriginalDraft.value = originalDraft.value;
    assessmentFinalDraft.value = finalDraft.value;
  }

  // Switch mode
  currentMode.value = mode;
  stats.value = { exchanges: 0, questions: 0, revisions: 0 };
  isOriginalDraftConfirmed.value = false;

  const chatMap = {
    training: trainingChatHistory,
    assessment: assessmentChatHistory,
  };

  if (mode in chatMap) {
    activeChatHistory.value = chatMap[mode].value;
    if (!chatMap[mode].value.length)
      chatMap[mode].value.push(makeChatHistoryEntry("assistant", greetings[mode]));

    // Load saved drafts for this mode
    originalDraft.value =
      mode === "training"
        ? trainingOriginalDraft.value || Sample_Essay
        : assessmentOriginalDraft.value || "";
    finalDraft.value = mode === "training" ? trainingFinalDraft.value : assessmentFinalDraft.value;
  } else {
    activeChatHistory.value = [];
  }
}

/* Sync draft changes to their mode-specific refs */
watch([originalDraft, finalDraft, currentMode], () => {
  if (currentMode.value === "training") {
    trainingOriginalDraft.value = originalDraft.value;
    trainingFinalDraft.value = finalDraft.value;
  } else if (currentMode.value === "assessment") {
    assessmentOriginalDraft.value = originalDraft.value;
    assessmentFinalDraft.value = finalDraft.value;
  }
});

/* ------------ Utilities ------------ */
const makeChatHistoryEntry = (role, content) => ({
  role,
  content,
  timestamp: new Date(),
});

const showNotification = (msg, type = "success") => {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
};

/* ------------ API and Chat ------------ */
async function connectAPI(auto = false) {
  if (!apiKey.value && !auto) return;
  localStorage.setItem("chatbot_api_key", apiKey.value);
  isConnecting.value = true;

  try {
    const reply = await talkToChatbot([
      { role: "system", content: "connection test, return 1" },
      { role: "user", content: "Hello!" },
    ]);
    isConnected.value = reply?.trim().length > 0;
    showNotification(
      isConnected.value ? "✅ Connected!" : "⚠️ No valid reply",
      isConnected.value ? "success" : "error"
    );
    if (isConnected.value && currentMode.value === "briefing") switchMode("training");
  } catch {
    showNotification("❌ Connection failed", "error");
  } finally {
    isConnecting.value = false;
  }
}

const clearAPI = () => {
  localStorage.removeItem("chatbot_api_key");
  apiKey.value = "";
  isConnected.value = false;
  activeChatHistory.value = [];
};

const confirmDraft = () => {
  if (!originalDraft.value.trim())
    return alert(
      currentMode.value === "assessment"
        ? "Please paste your essay first."
        : "Please paste the original draft first."
    );
  isOriginalDraftConfirmed.value = true;
  finalDraft.value = originalDraft.value;
};

/* ------------ Report Generation ------------ */
async function generateAssessmentReport(mode = "final") {
  isGeneratingAssessment.value = true;
  try {
    const data = {
      original: originalDraft.value || "(empty)",
      revised: finalDraft.value || "(empty)",
      chat: activeChatHistory.value.map(({ role, content, timestamp }) => ({
        role,
        content,
        timestamp,
      })),
    };

    const report = await talkToChatbot([
      { role: "system", content: `${AssessBot_Prompt}\n\n${JSON.stringify(data, null, 2)}` },
      { role: "user", content: makeReportTemplate(mode) },
    ]);

    hiddenReport.value = report;
    reportGenerationInstructions.value = makeReportHeader(mode, report);
    reportChatHistory.value = [
      makeChatHistoryEntry("system", `Original:\n${data.original}\n\nRevised:\n${data.revised}`),
      ...activeChatHistory.value,
    ];
    bccEmail.value = ["simonwanghkteacher@gmail.com"];
    showReport.value = true;
    showNotification(`📊 ${mode === "training" ? "Training" : "Assessment"} report generated!`);
  } catch (e) {
    console.error(e);
    showNotification("⚠️ Error generating report — fallback used", "error");
  } finally {
    isGeneratingAssessment.value = false;
  }
}

const makeReportTemplate = (mode) =>
  mode === "training"
    ? "Please provide a student training progress report emphasizing AI collaboration."
    : "Please provide a comprehensive assessment based on the essay and chat history.";

const makeReportHeader = (mode, body) =>
  `${
    mode === "training" ? "TRAINING" : "FINAL"
  } ASSESSMENT REPORT\n\n${body}\n\n(Do not mention scores.)`;

const submitAssessment = async () => {
  if (!isOriginalDraftConfirmed.value) return alert("Please confirm your original essay first.");
  userMessage.value = "done";
  await sendMessage();
  setTimeout(() => generateAssessmentReport("final"), 1000);
};

const confirmFinalDraft = async () => {
  if (!originalDraft.value.trim() || !finalDraft.value.trim())
    return alert("Please paste your final draft first.");
  await generateAssessmentReport("training");
};

/* ------------ Lifecycle ------------ */
const handleBeforeUnload = (e) => {
  if (!isSubmitted.value) {
    e.preventDefault();
    e.returnValue = "";
  }
};

onMounted(async () => {
  window.addEventListener("beforeunload", handleBeforeUnload);
  const saved = localStorage.getItem("chatbot_api_key");
  if (saved) {
    apiKey.value = saved;
    await connectAPI(true);
  }
  switchMode(currentMode.value);
});

onBeforeUnmount(() => window.removeEventListener("beforeunload", handleBeforeUnload));
</script>
