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
                    HKBU Generative AI Platform </a
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

      <!-- Submitted Course Info Display (Training Mode) -->
      <div
        v-if="currentMode == 'training' && hasSubmittedCourseInfo"
        class="mb-6 p-4 bg-gray-50 rounded-lg"
      >
        <h3 class="text-lg font-semibold mb-3 text-gray-800">📘 Course Information</h3>
        
        <!-- Info Alert about AI Sharing -->
        <div class="mb-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
          <p class="text-sm text-blue-900">
            <strong>ℹ️ Important:</strong> This course information has been shared with the AI tutor so it can provide contextually relevant feedback and guidance based on your course requirements.
          </p>
        </div>

        <!-- Read-only structured view -->
        <div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
          <h4 class="text-md font-semibold text-gray-700 mb-3">📋 Course Information (Read-only)</h4>
          <div class="overflow-x-auto">
            <table class="w-full text-sm border border-gray-200 rounded-lg">
              <tbody>
                <tr
                  v-for="(value, key) in courseInfo"
                  :key="key"
                  class="even:bg-gray-50 border-b border-gray-200"
                >
                  <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700 bg-gray-100">
                    {{ formatLabel(key) }}
                  </th>
                  <td class="px-4 py-2 text-gray-900">
                    {{ value || "—" }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Markdown Code Block -->
        <div class="bg-gray-900 rounded-lg p-4">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-md font-semibold text-gray-200">📝 Markdown Code (Copy this)</h4>
            <button
              @click="copyCourseInfoMarkdown"
              class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium px-3 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            >
              📋 Copy
            </button>
          </div>
          <pre class="text-xs text-green-400 overflow-x-auto whitespace-pre-wrap"><code>{{ getCourseInfoMarkdown() }}</code></pre>
        </div>
      </div>

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
      <BackgroundAndRubrics
        v-if="!hasSubmittedTrainingBackground && currentMode == 'training'"
        v-model:rubric="rubric"
        v-model:courseInfo="courseInfo"
        v-model:studentContext="studentContext"
        @submitCourseInfo="handleSubmitCourseInfo"
        @submitStudentContext="handleSubmitStudentContext"
        @submitRubric="handleSubmitRubrics"
      />
      <BackgroundAndRubrics
        v-if="!hasSubmittedAssessmentBackground && currentMode == 'assessment'"
        v-model:rubric="rubricAssessment"
        v-model:courseInfo="courseInfoAssessment"
        v-model:studentContext="studentContextAssessment"
        @submitCourseInfo="handleSubmitCourseInfo"
        @submitStudentContext="handleSubmitStudentContext"
        @submitRubric="handleSubmitRubrics"
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
          reportStudentContext,
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
const hasSubmittedCourseInfo = ref(false);
const hasSubmittedStudentContext = ref(false);
const showVideoTutorial = ref(false);
const rubric = ref(`## Assessment Task: Writing (20%)

### Rubrics

#### Part 1: Point-of-view Essay (10%)



| Criteria                                 |                                                   1 (Limited)                                                    |                                           2 (Basic)                                           |                                              3 (Developing)                                               |                                           4 (Proficient)                                           |                                                      5 (Excellent)                                                      |
| ---------------------------------------- | :--------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------: |
| **Content and Ideas**                    | Ideas are irrelevant or minimally related to the topic Lacks awareness of the issue concerned No clear viewpoint | Ideas are somewhat related but vagueMinimal awareness of the issue concernedViewpoint unclear | Ideas are relevant but basic Some awareness of the issue concerned Viewpoint present but weakly developed | Ideas are relevant and solid Good awareness of the issue concerned Clear viewpoint with some depth | Ideas are insightful and highly relevant; Strong awareness of the issue concerned; Well-developed, compelling viewpoint |
| **Organisation and Logical Progression** |                    No clear structure Ideas are disjointed with no development or progression                    |      Basic structure with unclear paragraphing Ideas are listed with little development       |         Clear structure with some paragraphing Ideas are developed but lack depth or logical flow         |   Well-organized with clear paragraphs Ideas are developed logically with good flow and support    |     Highly organized with effective paragraphing; Ideas are thoroughly developed with seamless, logical progression     |
| **Vocabulary**                           |                    Vocabulary is limited, repetitive, or inaccurateLacks topic-specific terms                    |           Basic vocabulary with some repetitionMinimal use of topic-specific terms            |    Adequate vocabulary with some varietyIncludes some topic-specific terms but with occasional errors     |          Varied and precise vocabulary Effective use of topic-specific terms Minor errors          |          Rich, precise vocabulary; Masterful use of topic-specific terms; Almost error-free and sophisticated           |
| **Grammar and Sentence Structure**       |                  Frequent grammatical and spelling errorsSentences are incomplete or confusing                   |         Several grammatical and spelling errorsSentences are simple and often flawed          |             Some grammatical and spelling errorsSentences are mostly correct but lack variety             |           Minor grammatical and spelling errorsSentences are varied and mostly accurate            |          Virtually error-free grammar and spelling; Sentences are complex, varied, and accurately constructed           |

---
## Task 2: AI-Assisted Review of Student Draft (10%)

In this task, students will independently engage in a conversation with a chatbot to revise their own draft essay, without any prompts provided. The focus is on learning how to critically assess and refine their work through interaction with the chatbot, improving the essay's overall quality based on the feedback received.

### Rubric for AI-Assisted Review

|Criteria|1 (Limited)|2 (Basic)|3 (Developing)|4 (Proficient)|5 (Excellent)|
|---|---|---|---|---|---|
|A. In-Depth Conversation with AI|No exchanges or chat history provided; no conversation beyond initial input; no questions asked|Sparse exchanges with incomplete or no chat history; basic conversation with one or two simple questions; lacks depth|Adequate exchanges shown in chat history; moderate conversation with some relevant questions; shows some depth|Robust exchanges with comprehensive chat history; in-depth conversation with detailed, relevant questions on all levels|Extensive exchanges with thorough, well-documented chat history; highly in-depth conversation with insightful, multi-level questions|
|B. Critical Review of AI Suggestions|All AI suggestions accepted without evaluation; no critical thought|Most AI suggestions accepted with little critical analysis|Some AI suggestions evaluated; partial critical review with justification|Most AI suggestions critically assessed; clear justification for choices|All AI suggestions thoroughly evaluated; strong, evidence-based justification|
|C. Refining Process|No revisions made|Minimal revisions with no iterative process|Some revisions with limited iteration based on AI feedback|Clear iterative process with multiple revisions based on AI input|Extensive refinement with critical review of AI feedback at each step|

`);
const courseInfo = ref({
  course: "LANG 0036 - English for Academic Purposes",
  level: "Intermediate to Advanced",
  focus: "Academic writing and critical thinking",
  assessment: "Essay writing with rubric-based evaluation",
});
const studentContext = ref({
  academicLevel: "University student",
  language: "English as additional language",
  goals: "Improve academic writing skills",
  challenges: "Structure, vocabulary, critical analysis",
});
const courseInfoAssessment = ref({
  course: "",
  level: "",
  focus: "",
  assessment: "",
});
const rubricAssessment = ref("");
const studentContextAssessment = ref({
  academicLevel: "",
  language: "",
  goals: "",
  challenges: "",
});
const reprotInfo = ref("");
const reportStudentContext = ref("");

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
  rubric,
  studentContext,
  courseInfo,
  rubricAssessment,
  studentContextAssessment,
  courseInfoAssessment,
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

const formatLabel = (key) => {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
};

const getCourseInfoMarkdown = () => {
  const md = Object.entries(courseInfo.value)
    .map(([k, v]) => `- **${formatLabel(k)}:** ${v || "—"}`)
    .join("\n");
  return `### 📘 Course Information\n${md}`;
};

const copyCourseInfoMarkdown = () => {
  navigator.clipboard.writeText(getCourseInfoMarkdown()).then(() => {
    Swal.fire({
      text: "Course information copied to clipboard as Markdown!",
      icon: "success",
    });
  });
};

const showNotification = (msg, type = "success") => {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
};
function handleSubmitCourseInfo(newCourseInfo) {
  if (currentMode.value == "assessment") {
    Object.assign(courseInfoAssessment.value, newCourseInfo);
    Swal.fire({
      title: "Course Information Submitted!",
      text: "The information is sent to AI tutor. You may download a markdown copy for your records.",
      icon: "success",
    });
  } else {
    Object.assign(courseInfo.value, newCourseInfo);
    hasSubmittedCourseInfo.value = true;
    Swal.fire({
      title: "Course Information Submitted!",
      text: "The information is sent to AI tutor. You may download a markdown copy for your records.",
      icon: "success",
    });
  }
}

function handleSubmitStudentContext(newStudentContext) {
  if (currentMode.value == "assessment") {
    Object.assign(studentContextAssessment.value, newStudentContext);
    Swal.fire({
      title: "Student Context Submitted!",
      text: "The information is sent to AI tutor. You may download a markdown copy for your records.",
      icon: "success",
    });
  } else {
    Object.assign(studentContext.value, newStudentContext);
    hasSubmittedStudentContext.value = true;
    Swal.fire({
      title: "Student Context Submitted!",
      text: "The information is sent to AI tutor. You may download a markdown copy for your records.",
      icon: "success",
    });
  }
}
function handleSubmitRubrics(newRubric) {
  if (currentMode.value == "assessment") {
    rubricAssessment.value = newRubric;
    hasSubmittedAssessmentBackground.value = true;
    Swal.fire({
      title: "Rubrics Submitted!",
      text: "The information is sent to AI tutor.",
      icon: "success",
    });
  } else {
    rubric.value = newRubric;
    hasSubmittedTrainingBackground.value = true;
    navigator.clipboard.writeText(rubric.value);
    Swal.fire({
      title: "Rubrics Submitted!",
      text: `The Rubrics have been submitted. Please note that this is training mode, so the
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

                    If the student has not completed any of the above tasks, then return and only return '109'.

                    If the student has completed all targets, then execute the following: 
                    ${AssessBot_Prompt}\n\n${JSON.stringify(data, null, 2)}`,
      },
      { role: "user", content: makeReportTemplate(mode) },
    ]);
    if (report.includes("109")) {
      Swal.fire({
        text: "It seems that you have not revised all the required components (thesis statement, topic sentence, body paragraph). Please make sure to complete these revisions before generating the report.",
        icon: "warning",
      });
      isGeneratingAssessment.value = false;
      return;
    }
    hiddenReport.value = report;
    reportGenerationInstructions.value = makeReportHeader(mode, report);
    reportChatHistory.value = [
      makeChatHistoryEntry("system", `Original:\n${data.original}\n\nRevised:\n${data.revised}`),
      ...activeChatHistory.value,
    ];
    bccEmail.value = ["simonwanghkteacher@gmail.com", "21253153@life.hkbu.edu.hk"];
    if (currentMode.value === "training") {
      reportStudentContext.value = studentContext.value;
      reprotInfo.value = courseInfo.value;
    } else if (currentMode.value === "assessment") {
      reportStudentContext.value = studentContextAssessment.value;
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
