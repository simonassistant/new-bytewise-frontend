<template>
  <div class="w-full p-4 flex-1 flex flex-col">
    <!-- Main Header for All Modes -->
    <div class="text-center mb-6">
      <h1 class="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 bg-clip-text text-transparent">
        LANG 0036: AI Writing Collaboration Lab
      </h1>
      <p class="text-lg bg-gradient-to-r from-gray-600 via-blue-500 to-purple-500 bg-clip-text text-transparent">
        Develop and demonstrate AI literacy and human-AI partnership through guided essay revision and assessment
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
      <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
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
                {{ currentMode === 'assessment' ? 'Your Original Essay' : 'Original Draft' }}
              </h2>
              <textarea
                v-model="originalDraft"
                rows="6"
                :placeholder="currentMode === 'assessment' ? 'Paste your original essay here...' : 'Paste or write the original draft here...'"
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                :disabled="isOriginalDraftConfirmed"
              ></textarea>
              <button
                @click="confirmDraft"
                class="w-full mt-2 px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isOriginalDraftConfirmed"
              >
                {{ isOriginalDraftConfirmed ? "Essay Confirmed" : (currentMode === 'assessment' ? "Confirm Your Essay" : "Confirm Original Draft") }}
              </button>
            </div>

            <!-- Final Draft -->
            <div class="bg-white p-4 rounded-lg shadow">
              <h2 class="text-lg font-bold mb-2">
                {{ currentMode === 'assessment' ? 'Revised Version (Auto-Updated)' : 'Final Draft' }}
              </h2>
              <textarea
                v-model="finalDraft"
                rows="6"
                :placeholder="currentMode === 'assessment' ? 'This will be updated automatically as you revise through chat...' : 'Paste or write the improved draft here...'"
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                :disabled="currentMode === 'assessment' ? isOriginalDraftConfirmed : !isOriginalDraftConfirmed"
                :readonly="currentMode === 'assessment'"
              ></textarea>
              <button
                @click="currentMode === 'assessment' ? submitAssessment() : confirmFinalDraft()"
                class="w-full mt-2 px-3 py-2 text-white rounded-lg text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                :class="currentMode === 'assessment' ? 'bg-green-600' : 'bg-blue-600'"
                :disabled="!isOriginalDraftConfirmed || isGeneratingAssessment"
              >
                <span v-if="isGeneratingAssessment">
                  {{ currentMode === 'assessment' ? '🔄 Generating Assessment...' : '🔄 Generating Report...' }}
                </span>
                <span v-else>
                  {{ currentMode === 'assessment' ? 'Submit Assessment' : 'Confirm Final Draft & Generate Report' }}
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
      bccEmail,
      ccEmail,
    }"
    @close="showReport = false"
  />
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { BASE_URL } from "../components/base_url";
import MarkdownIt from "markdown-it";
import BriefMode from "@/components/writing_bot/BriefMode.vue";
import ReportModal from "../components/ReportModal.vue";
import { Sample_Essay } from "@/components/writing_bot/sampleEssay.js";
import { Trainging_Mode_Prompt } from "@/components/writing_bot/sampleEssay.js";
import { Assessment_Mode_Prompt } from "@/components/writing_bot/sampleEssay.js";
import { AssessBot_Prompt } from "@/components/writing_bot/sampleEssay.js";

// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
/* ------------ State ------------ */
const currentMode = ref("briefing");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });
const originalDraft = ref("");  // Start empty for assessment mode
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

const greetings = {
  training: `Thanks for sharing the essay! Tell me about your course and what help you need.

I'm here to help you learn 4 essential AI collaboration skills while we work together to revise this climate change essay:

✅ **Skill 1**: Provide contextual information to AI
✅ **Skill 2**: Strategic planning and goal negotiation
✅ **Skill 3**: Critical review of AI suggestions
✅ **Skill 4**: Independent editing and decision-making

**Here's the sample essay we'll be working on:**

---

**Essay Question**: Some people believe that individual actions are insignificant in the fight against climate change compared to the efforts of governments and large corporations. To what extent do you agree or disagree with this statement?

**Sample Essay** (Current Version - Needs Improvement):

Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.

Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don't know sometimes.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.

---

To help you effectively, I'd like to know:
- What course are you taking?
- What are your goals for this revision session?
- Are you familiar with the assessment rubrics?

Once I understand your context, we'll work together to improve this essay. Remember: I'll guide you and make suggestions, but YOU will do all the actual editing. Let's begin! 🚀`,
  assessment: `Hello! I'm ready to help you revise your essay. Please paste your original essay in the "Your Original Essay" box and click "Confirm Your Essay" to begin.

Here's how assessment mode works:

📝 **Step 1**: Paste your original essay and confirm it (the box will become locked)
💬 **Step 2**: Tell me what help you need and start our revision conversation
🔄 **Step 3**: I'll automatically update your "Revised Version" as we work together
🏁 **Step 4**: When you're satisfied, click "Submit Assessment" to finish

Remember: This is assessment mode, so you'll need to take the lead in our conversation. I'm here to provide suggestions and feedback, but you'll need to:

• Provide context about your assignment and goals
• Ask for specific feedback on areas you want to improve
• Guide our revision process through the chat
• Make final decisions about which suggestions to implement

I'll track the latest version of your essay automatically as we discuss improvements. Let's begin!`,
  briefing: `Welcome to LANG 0036: AI Writing Collaboration Lab! Please configure your API settings to start using the system.`,
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
      activeChatHistory.value.push({ role: "assistant", content: reply, timestamp: new Date() });

      // In assessment mode, try to extract updated essay text from AI response
      if (currentMode.value === "assessment" && isOriginalDraftConfirmed.value) {
        extractAndUpdateEssay(reply);
      }

      scrollToBottom();
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

function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  });
}

// Function to extract and update essay from AI response in assessment mode
function extractAndUpdateEssay(aiResponse) {
  // Look for common patterns that indicate a revised essay
  const patterns = [
    /(?:Here'?s the revised version|Updated essay|Revised essay|Here'?s your improved essay)[:\s]*([\s\S]*?)(?:\n\n|$)/i,
    /(?:Revised version|Updated version)[:\s]*([\s\S]*?)(?:\n\n|$)/i,
    /```([\s\S]*?)```/,  // Text in code blocks
    /"([\s\S]*?)"/,      // Text in quotes (if it's longer than 100 chars)
  ];

  for (const pattern of patterns) {
    const match = aiResponse.match(pattern);
    if (match && match[1] && match[1].trim().length > 100) {
      // Only update if we found substantial text (>100 chars)
      const extractedText = match[1].trim();
      if (extractedText !== finalDraft.value) {
        finalDraft.value = extractedText;
        // Show a brief notification that the essay was updated
        showNotification("📝 Essay updated automatically", "success");
        break;
      }
    }
  }
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
    alert(currentMode.value === "assessment" ? "Please paste your original essay first." : "Please paste the original draft first.");
  }
}

async function submitAssessment() {
  if (isOriginalDraftConfirmed.value && originalDraft.value.trim()) {
    // Send "done" message to end assessment session
    userMessage.value = "done";
    await sendMessage();

    // Generate comprehensive assessment report using AssessBot after a short delay
    setTimeout(async () => {
      isGeneratingAssessment.value = true;
      try {
        // Prepare the assessment data for AssessBot
        const assessmentData = {
          originalEssay: originalDraft.value,
          revisedEssay: finalDraft.value,
          chatHistory: activeChatHistory.value.map(msg => ({
            role: msg.role,
            content: msg.content,
            timestamp: msg.timestamp
          }))
        };

        // Create the system prompt for AssessBot with the assessment data
        const assessmentSystemMessage = {
          role: "system",
          content: AssessBot_Prompt +
            "\n\nOriginal Essay:\n---\n" + assessmentData.originalEssay +
            "\n---\n\nRevised Essay:\n---\n" + assessmentData.revisedEssay +
            "\n---\n\nChat History:\n" +
            JSON.stringify(assessmentData.chatHistory, null, 2)
        };

        // Send assessment request to AssessBot
        const assessmentResponse = await fetch(`${BASE_URL}/chatbot/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_history: [
              assessmentSystemMessage,
              {
                role: "user",
                content: "Please provide a comprehensive assessment report for this student's performance based on the provided original essay, revised essay, and chat history. Follow the structured format specified in your system prompt."
              }
            ],
            api_key: apiKey.value,
            model_name: model.value,
          }),
        });

        const assessmentData_response = await assessmentResponse.json();
        const assessmentReport = assessmentData_response?.choices?.[0]?.message?.content ||
                               assessmentData_response?.response ||
                               assessmentData_response?.message ||
                               "Error generating assessment report";

        // Update report generation instructions with the AssessBot report
        reportGenerationInstructions.value = `COMPREHENSIVE STUDENT ASSESSMENT REPORT

Generated by AssessBot using dual rubric assessment:

${assessmentReport}

This report evaluates both essay writing improvement and human-AI collaboration skills according to LANG 0036 course rubrics.`;

        bccEmail.value = ["simonwanghkteacher@gmail.com"];
        reportChatHistory.value = [
          {
            role: "system",
            content:
              "Original Essay:\n---\n" +
              `${originalDraft.value || "(empty)"}\n---\n\n` +
              "Revised Essay:\n---\n" +
              `${finalDraft.value || "(empty)"}\n---\n\n` +
              "Assessment Report:\n---\n" +
              assessmentReport + "\n---\n",
            timestamp: new Date(),
          },
          ...activeChatHistory.value,
        ];

        showReport.value = true;
        showNotification("📊 Assessment report generated successfully!", "success");

      } catch (error) {
        console.error("Error generating assessment report:", error);
        showNotification("⚠️ Error generating assessment report. Using fallback.", "error");

        // Fallback to original simple report
        bccEmail.value = ["simonwanghkteacher@gmail.com"];
        reportChatHistory.value = [
          {
            role: "system",
            content:
              "Original Essay:\n---\n" +
              `${originalDraft.value || "(empty)"}\n---\n\n` +
              "Final Essay:\n---\n" +
              `${finalDraft.value || "(empty)"}\n---\n\n`,
            timestamp: new Date(),
          },
          ...activeChatHistory.value,
        ];
        showReport.value = true;
      } finally {
        isGeneratingAssessment.value = false;
      }
    }, 1000);
  } else {
    alert("Please confirm your original essay first.");
  }
}

async function confirmFinalDraft() {
  if (isOriginalDraftConfirmed.value && originalDraft.value.trim() && finalDraft.value.trim()) {
    isGeneratingAssessment.value = true;
    try {
      // Generate assessment report using AssessBot for training mode as well
      const assessmentData = {
        originalEssay: originalDraft.value,
        revisedEssay: finalDraft.value,
        chatHistory: activeChatHistory.value.map(msg => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp
        }))
      };

      // Create the system prompt for AssessBot with the assessment data
      const assessmentSystemMessage = {
        role: "system",
        content: AssessBot_Prompt +
          "\n\nOriginal Essay:\n---\n" + assessmentData.originalEssay +
          "\n---\n\nRevised Essay:\n---\n" + assessmentData.revisedEssay +
          "\n---\n\nChat History:\n" +
          JSON.stringify(assessmentData.chatHistory, null, 2)
      };

      // Send assessment request to AssessBot
      const assessmentResponse = await fetch(`${BASE_URL}/chatbot/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_history: [
            assessmentSystemMessage,
            {
              role: "user",
              content: "Please provide a comprehensive assessment report for this student's training performance based on the provided original essay, revised essay, and chat history. Focus on both essay improvement and demonstration of AI collaboration skills during training."
            }
          ],
          api_key: apiKey.value,
          model_name: model.value,
        }),
      });

      const assessmentData_response = await assessmentResponse.json();
      const assessmentReport = assessmentData_response?.choices?.[0]?.message?.content ||
                             assessmentData_response?.response ||
                             assessmentData_response?.message ||
                             "Error generating assessment report";

      // Update report generation instructions with the AssessBot report
      reportGenerationInstructions.value = `TRAINING MODE ASSESSMENT REPORT

Generated by AssessBot for training completion:

${assessmentReport}

This report shows the student's progress in learning AI collaboration skills and essay revision during training mode.`;

      bccEmail.value = ["simonwanghkteacher@gmail.com"];
      reportChatHistory.value = [
        {
          role: "system",
          content:
            "Original Essay:\n---\n" +
            `${originalDraft.value || "(empty)"}\n---\n\n` +
            "Revised Essay:\n---\n" +
            `${finalDraft.value || "(empty)"}\n---\n\n` +
            "Training Assessment Report:\n---\n" +
            assessmentReport + "\n---\n",
          timestamp: new Date(),
        },
        ...activeChatHistory.value,
      ];

      showReport.value = true;
      showNotification("📊 Training assessment report generated!", "success");

    } catch (error) {
      console.error("Error generating training assessment report:", error);
      showNotification("⚠️ Error generating assessment report. Using fallback.", "error");

      // Fallback to original simple report
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
