<template>
  <div class="w-full p-4 flex-1 flex flex-col">
    <!-- Header -->
    <CourseHeader />
    <!-- Mode Selection -->
    <ModeSelector
      :currentMode="currentMode"
      :isThinking="isThinking"
      :modeLabels="modeLabels"
      :modeColors="modeColors"
      :is-open="isModeSelectorOpen"
      @switch-mode="switchMode"
      @toggle-open="isModeSelectorOpen = $event"
    />
    <div
      class="flex-1 transition-all duration-500 ease-in-out p-4"
      :class="isModeSelectorOpen ? 'ml-64' : 'ml-0'"
    >
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
                    HKBU Generative AI Platform (click here) </a
                  >.
                </p>
                <button
                  @click="showVideoTutorial = !showVideoTutorial"
                  class="mt-3 text-xs text-indigo-600 hover:text-indigo-800 underline"
                >
                  {{ showVideoTutorial ? "▼ Hide" : "▶ Show" }} Tutorial Slides
                </button>
                <div v-if="showVideoTutorial" class="mt-3">
                  <iframe
                    src="https://scribehow.com/embed/Generate_an_API_Key_for_AI_Tutor__GPd3vfdkR6mghvEFGAHeog"
                    width="100%"
                    height="800"
                    allow="fullscreen"
                    style="aspect-ratio: 1 / 1; border: 0; min-height: 480px"
                    title="API Key Setup Tutorial"
                  />
                </div>
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
      <BackgroundAndRubrics
        v-if="currentMode == 'training'"
        v-model:courseInfo="courseInfo"
        v-model:currentMode="currentMode"
        v-model:isShowArea="isTrainingBackgroundAreaVisible"
        v-model:isSubmitted="hasSubmittedTrainingBackground"
        @submitAll="handleSubmitRubrics"
        @toggleArea="isTrainingBackgroundAreaVisible = $event"
      />
      <BackgroundAndRubrics
        v-if="currentMode == 'assessment'"
        v-model:courseInfo="courseInfoAssessment"
        v-model:currentMode="currentMode"
        v-model:isShowArea="isAssessmentBackgroundAreaVisible"
        v-model:isSubmitted="hasSubmittedAssessmentBackground"
        @submitAll="handleSubmitRubrics"
        @toggleArea="isAssessmentBackgroundAreaVisible = $event"
      />
      <!-- Chat Interface -->
      <ChatInterface
        v-if="
          (currentMode == 'training' && hasSubmittedTrainingBackground) ||
          (currentMode == 'assessment' && hasSubmittedAssessmentBackground)
        "
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
        :bulletPoints="bulletPoints"
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
          reprotInfo,
        }"
        @close="showReport = false"
        @submit="
          {
            isSubmitted = true;
            showReport = false;
          }
        "
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import BriefMode from "@/components/new_EEGC/BriefMode.vue";
import ReportModal from "@/components/new_EEGC/WritingBotReport.vue";
import ChatInterface from "@/components/new_EEGC/ChatInterface.vue";
import CourseHeader from "@/components/new_EEGC/CourseHeader.vue";
import ModeSelector from "@/components/new_EEGC/ModeSelector.vue";
import BackgroundAndRubrics from "@/components/new_EEGC/BackgroundAndRubrics.vue";
import { useChatFunctions } from "@/components/new_EEGC/useChatFunctions";
import Swal from "sweetalert2";

import {
  Sample_Essay,
  AssessBot_Prompt,
  Training_Greetings,
  Assessment_Greetings,
  Rubric,
} from "@/components/new_EEGC/promptAndEssay.js";

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
const isModeSelectorOpen = ref(true);
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
const bulletPoints = ref("No bullet points extracted yet.");
const hasSubmittedTrainingBackground = ref(false);
const hasSubmittedAssessmentBackground = ref(false);
const showVideoTutorial = ref(false);
const rubric = ref(Rubric);
const isTrainingModeFinished = ref(false);
const isTrainingBackgroundAreaVisible = ref(true);
const isAssessmentBackgroundAreaVisible = ref(true);
const courseInfo = ref(`Course Information:
Course: LANG 0036 - English for Academic Purposes
Level: Intermediate to Advanced
Focus: Academic writing and critical thinking
Assessment: Essay writing with rubric-based evaluation\n
Student Background:
AcademicLevel: University student
Language: English as additional language
Goals: Improve academic writing skills
Challenges: Structure, vocabulary, critical analysis\n
Rubric:
${Rubric}`);

const courseInfoAssessment = ref(`
  Course Information:
  Course: 
  Level: 
  Focus: 
  Assessment: \n
  Student Background:
  AcademicLevel: 
  Language: 
  Goals: 
  Challenges: \n
  Rubric:
`);

const reprotInfo = ref("");

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
  bulletPoints,
  isConnected,
  apiKey,
  model,
  isThinking,
  isOriginalDraftConfirmed,
  isUpdatingDraft,
  courseInfo,
  courseInfoAssessment,
});

/* ------------ Mode Switching ------------ */
function switchMode(mode) {
  // Save current drafts before switching
  if (mode == "assessment") {
    Swal.fire({
      text: "The assessment mode is not yet open. It will open from 14 November to 01 December. Please contact ZHANG_KT@hkbu.edu.hk for enquiries.",
      icon: "warning",
    });
    return;
  }
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
  if (mode == "training") isOriginalDraftConfirmed.value = true;
  else isOriginalDraftConfirmed.value = false;

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

function handleSubmitRubrics(newBackground) {
  if (currentMode.value == "assessment") {
    hasSubmittedAssessmentBackground.value = true;
    courseInfoAssessment.value = newBackground;
    Swal.fire({
      title: "Rubrics Submitted!",
      text: "The information is sent to AI tutor.",
      icon: "success",
    });
  } else {
    hasSubmittedTrainingBackground.value = true;
    courseInfo.value = newBackground;
    navigator.clipboard.writeText(rubric.value);
    Swal.fire({
      title: "Rubrics Submitted!",
      text: `The informationhave been submitted. Please note that this is training mode, so the
      information has been pre-filled for your convenience. You will be required to enter it
      manually in assessment mode. The rubrics have also been copied to your clipboard for easy pasting later.`,
      icon: "success",
    });
  }
}

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
      {
        role: "system",
        content: ` 
                  Check whether the student has completed the following tasks:
                    1. Revised the thesis statement  
                    2. Revised one of the topic sentence  
                    3. Revised one of the body paragraph  

                    If the student has not completed any of the above tasks, then you should say 'not finished'.

                    Then execute the following: 
                    ${AssessBot_Prompt}\n\n${JSON.stringify(data, null, 2)}`,
      },
      { role: "user", content: makeReportTemplate(mode) },
    ]);
    if (report.includes("not finished")) {
      Swal.fire({
        text: "It seems that you have not revised all the required components (thesis statement, topic sentence, body paragraph). Please make sure to complete these revisions before generating the report.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        reverseButtons: true, // Optional: makes "No" appear first for clarity
      }).then((result) => {
        if (!result.isConfirmed) {
          // If the user clicked "No", do nothing (just return)
          return;
        }
      });
      isGeneratingAssessment.value = false;
    }
    hiddenReport.value = report;
    isTrainingModeFinished.value = true;
    reportGenerationInstructions.value = makeReportHeader(mode, report);
    reportChatHistory.value = [
      makeChatHistoryEntry("system", `Original:\n${data.original}\n\nRevised:\n${data.revised}`),
      ...activeChatHistory.value,
    ];
    bccEmail.value = ["simonwanghkteacher@gmail.com", "21253153@life.hkbu.edu.hk"];
    if (currentMode.value === "training") {
      reprotInfo.value = courseInfo.value;
    } else if (currentMode.value === "assessment") {
      reprotInfo.value = courseInfoAssessment.value;
    }
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
    Swal.fire({
      text: "You have not sent the report yet. Please make sure to submit before leaving.",
      icon: "warning",
    });
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
