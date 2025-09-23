<template>
  <div class="bg-white text-gray-900 transition-colors duration-300 min-h-screen flex flex-col">
    <div class="container mx-auto max-w-6xl p-4 flex-1">
      <!-- Header -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold mb-2">EEGC Human-AI Collaboration Chatbot</h1>
        <p class="text-gray-600">Practice and assess your AI interaction skills</p>
      </div>

      <!-- Mode Selection -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="flex gap-4">
            <button
              @click="switchMode('briefing')"
              :class="currentMode === 'briefing' ? activeBtn : inactiveBtn"
            >
              Briefing Mode
            </button>
            <button
              @click="switchMode('training')"
              :class="currentMode === 'training' ? activeBtn : inactiveBtn"
            >
              Training Mode
            </button>
            <button
              @click="switchMode('assessment')"
              :class="currentMode === 'assessment' ? activeBtn : inactiveBtn"
            >
              Assessment Mode
            </button>
          </div>
          <div
            class="px-4 py-2 rounded-full text-sm font-medium"
            :class="
              {
                'bg-green-100 text-green-800': currentMode === 'training',
                'bg-red-100 text-red-800': currentMode === 'assessment',
                'bg-blue-100 text-blue-800': currentMode === 'briefing'
              }
            "
          >
            {{ currentMode === "training" ? "Training Mode Active" : currentMode === "assessment" ? "Assessment Mode Active" : "Briefing Mode Active" }}
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <!-- Training Mode and Assessment Mode -->
      <div
        v-if="currentMode === 'training' || currentMode === 'assessment'"
        class="gap-6 mb-6 grid"
        :class="currentMode === 'assessment' ? 'md:grid-cols-3' : 'md:grid-cols-2'"
      >
        <!-- Left: Skills and Progress -->
        <div class="md:col-span-2 space-y-6">
          <!-- Skills Dashboard -->
          <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2
                class="text-xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent"
              >
                Skills Being Developed
              </h2>

              <SkillBadge
                borderColor="border-blue-500"
                title="In-Depth Conversation"
                textColor="text-blue-600"
                :points="[
                  'Ask follow-up questions',
                  'Engage in multi-level dialogue',
                  'Maintain conversation depth',
                ]"
              />
              <SkillBadge
                borderColor="border-purple-500"
                title="Critical Review"
                textColor="text-purple-600"
                :points="[
                  'Evaluate AI suggestions critically',
                  'Provide evidence-based justification',
                  'Accept/reject with reasoning',
                ]"
              />
              <SkillBadge
                borderColor="border-green-500"
                title="Iterative Refinement"
                textColor="text-green-600"
                :points="[
                  'Multiple revision cycles',
                  'Build on previous feedback',
                  'Progressive improvement',
                ]"
              />
            </div>

            <!-- Session Progress -->
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2 class="text-xl font-bold mb-4">Session Progress</h2>
              <div class="space-y-3">
                <SessionStat label="Total Exchanges" :value="stats.exchanges" color="blue" />
                <SessionStat label="Follow-up Questions" :value="stats.questions" color="purple" />
                <SessionStat label="Revision Cycles" :value="stats.revisions" color="green" />
              </div>
              <button
                @click="exportChatHistory"
                class="w-full mt-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:opacity-90 transition-opacity"
              >
                Export Chat History
              </button>
            </div>
          </div>

          <!-- Sample Essay -->
          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-bold mb-2">Sample Essay for Practice:</h3>
            <div class="text-sm bg-white p-4 rounded border italic">
              "As a university student, I agree with that internet has positive impact on our lives.
              During the Covid-19, schools were using Zoom to maintain their teaching. Until now,
              students had discovered many side of zoom. They use zoom to take tutorial classes,
              have meeting with group mates and so on. Internet not only allow students to study at
              home, but also provide a new learning style. Apart from that, the internet is also
              contributes to our health. With the rapid development of the 5G technology, doctors
              are able to operate more precisely Robot-Assist surgery (RAs). This means we can have
              less trauma, less covery time and better surgery effect. And it all thanks to the high
              speed and stable internet. Some people may worried about their privacy issue while
              using the internet. However, in my opinion, as long as we pay more attention to our
              behaviour such as not viewing strange website, not giving out our personal information
              and so on. We can protect our privacy to a certain extent. (170 words)"
            </div>
          </div>
        </div>

        <!-- Right: Assessment Inputs -->
        <div v-if="currentMode === 'assessment'" class="space-y-6">
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-lg font-bold mb-2">Original Draft</h2>
            <textarea
              v-model="originalDraft"
              rows="8"
              placeholder="Paste or write the original draft here..."
              class="w-full border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-lg font-bold mb-2">Final Draft</h2>
            <textarea
              v-model="finalDraft"
              rows="8"
              placeholder="Paste or write the improved draft here..."
              class="w-full border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Briefing Mode -->
      <div v-else class="max-w-6xl mx-auto p-6">
        <div class="space-y-8">
            <div class="text-center mb-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-2">Writing Assessment Tasks</h1>
                <p class="text-gray-600">Detailed rubrics and guidelines for assessment</p>
            </div>

            <div class="bg-white rounded-lg shadow-lg p-6 space-y-6">
                <div class="border-l-4 border-blue-500 pl-4">
                    <h2 class="text-xl font-bold text-blue-600 mb-2">Task 1: Point-of-View Essay with Guided Chatbot Revision (10%)</h2>
                    <p class="text-gray-700 leading-relaxed">In this task, students will engage in a conversation with a chatbot to revise a teacher-provided draft essay. The chatbot will provide appropriate prompts to guide the discussion, helping students identify areas for improvement and refine the draft into a stronger point-of-view essay. The goal is to enhance the essay's content, organization, vocabulary, and grammar through interactive feedback.</p>
                </div>

                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Rubric for Point-of-View Essay</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden shadow-sm">
                            <thead>
                                <tr class="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                                    <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Criteria</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">1 (Limited)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">2 (Basic)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">3 (Developing)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">4 (Proficient)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">5 (Excellent)</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm">
                                <tr class="hover:bg-blue-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">A. Content and Ideas</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Ideas are irrelevant or minimally related to the topic; lacks awareness of the issue; no clear viewpoint</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Ideas are somewhat related but vague; minimal awareness of the issue; viewpoint unclear</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Ideas are relevant but basic; some awareness of the issue; viewpoint present but weakly developed</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Ideas are relevant and solid; good awareness of the issue; clear viewpoint with some depth</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Ideas are insightful and highly relevant; strong awareness of the issue; well-developed, compelling viewpoint</td>
                                </tr>
                                <tr class="hover:bg-blue-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">B. Organisation and Logical Progression</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">No clear structure; ideas are disjointed with no development or progression</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Basic structure with unclear paragraphing; ideas are listed with little development</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Clear structure with some paragraphing; ideas are developed but lack depth or logical flow</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Well-organised with clear paragraphs; ideas are developed logically with good flow and support</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Highly organised with effective paragraphing; ideas are thoroughly developed with seamless, logical progression</td>
                                </tr>
                                <tr class="hover:bg-blue-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">C. Vocabulary</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Vocabulary is limited, repetitive, or inaccurate; lacks topic-specific terms</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Basic vocabulary with some repetition; minimal use of topic-specific terms</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Adequate vocabulary with some variety; includes some topic-specific terms but with occasional errors</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Varied and precise vocabulary; effective use of topic-specific terms; minor errors</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Rich, precise vocabulary; masterful use of topic-specific terms; almost error-free and sophisticated</td>
                                </tr>
                                <tr class="hover:bg-blue-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">D. Grammar and Sentence Structure</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Frequent grammatical and spelling errors; sentences are incomplete or confusing</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Several grammatical and spelling errors; sentences are simple and often flawed</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Some grammatical and spelling errors; sentences are mostly correct but lack variety</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Minor grammatical and spelling errors; sentences are varied and mostly accurate</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Virtually error-free grammar and spelling; sentences are complex, varied, and accurately constructed</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-lg p-6 space-y-6">
                <div class="border-l-4 border-purple-500 pl-4">
                    <h2 class="text-xl font-bold text-purple-600 mb-2">Task 2: AI-Assisted Review of Student Draft (10%)</h2>
                    <p class="text-gray-700 leading-relaxed">In this task, students will independently engage in a conversation with a chatbot to revise their own draft essay, without any prompts provided. The focus is on learning how to critically assess and refine their work through interaction with the chatbot, improving the essay's overall quality based on the feedback received.</p>
                </div>

                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Rubric for AI-Assisted Review</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden shadow-sm">
                            <thead>
                                <tr class="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
                                    <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Criteria</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">1 (Limited)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">2 (Basic)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">3 (Developing)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">4 (Proficient)</th>
                                    <th class="border border-gray-300 px-4 py-3 text-center font-semibold">5 (Excellent)</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm">
                                <tr class="hover:bg-purple-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">A. In-Depth Conversation with AI</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">No exchanges or chat history provided; no conversation beyond initial input; no questions asked</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Sparse exchanges with incomplete or no chat history; basic conversation with one or two simple questions; lacks depth</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Adequate exchanges shown in chat history; moderate conversation with some relevant questions; shows some depth</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Robust exchanges with comprehensive chat history; in-depth conversation with detailed, relevant questions on all levels</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Extensive exchanges with thorough, well-documented chat history; highly in-depth conversation with insightful, multi-level questions</td>
                                </tr>
                                <tr class="hover:bg-purple-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">B. Critical Review of AI Suggestions</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">All AI suggestions accepted without evaluation; no critical thought</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Most AI suggestions accepted with little critical analysis</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Some AI suggestions evaluated; partial critical review with justification</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Most AI suggestions critically assessed; clear justification for choices</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">All AI suggestions thoroughly evaluated; strong, evidence-based justification</td>
                                </tr>
                                <tr class="hover:bg-purple-50 transition-colors">
                                    <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">C. Refining Process</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">No revisions made</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Minimal revisions with no iterative process</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Some revisions with limited iteration based on AI feedback</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Clear iterative process with multiple revisions based on AI input</td>
                                    <td class="border border-gray-300 px-4 py-3 text-gray-700">Extensive refinement with critical review of AI feedback at each step</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Chatbot Section -->
    <div v-if="currentMode === 'training' || currentMode === 'assessment'" class="border-t bg-gray-50 p-4">
      <div class="max-w-6xl mx-auto flex flex-col h-96">
        <!-- Message list -->
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
                class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
                v-html="renderMarkdown(msg.content)"
              />
              <div class="text-xs text-gray-400 mt-2 text-right">
                {{ msg.timestamp.toLocaleTimeString() }}
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="mt-2 flex gap-2">
          <input
            v-model="userMessage"
            type="text"
            placeholder="Type your message..."
            class="flex-1 border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            @keyup.enter="sendMessage"
            :disabled="isThinking"
          />
          <button
            @click="sendMessage"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isThinking"
          >
            {{ isThinking ? "Thinking..." : "Send" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Connect Chatbot Section -->
    <div v-else class="container mx-auto max-w-6xl p-4">
      <!-- API Configuration Bar -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <div class="text-center mb-4">
          <h2 class="text-xl font-bold text-gray-900 mb-1">Connect to Chatbot</h2>
          <p class="text-gray-600 text-sm">Configure your API settings to start using the chatbot</p>
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
              >
                HKBU Generative AI Platform
              </a>.
            </p>
          </div>

          <!-- Model Selector -->
          <div class="flex-1 bg-gray-100 border border-gray-200 rounded-lg p-3">
            <h3 class="font-semibold mb-2 text-sm">🤖 Choose Model</h3>
            <select
              :value="model"
              @change="model = $event.target.value"
              class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
            >
              <option value="gpt-5-mini">GPT-5 Mini</option>
              <option value="gpt-5">GPT-5</option>
              <option value="gpt-4.1-mini">GPT-4.1 Mini</option>
              <option value="gpt-4.1">GPT-4.1</option>
            </select>
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
        <div v-if="notification.visible" class="mt-3 p-3 rounded-lg text-sm text-center" :class="notification.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          {{ notification.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h, defineComponent, nextTick, onMounted } from "vue";
import { BASE_URL } from "../components/base_url";
import MarkdownIt from "markdown-it";

// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
/* ------------ State ------------ */
const currentMode = ref("briefing");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });
const originalDraft = ref("");
const finalDraft = ref("");

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

/* ------------ Components ------------ */
const SkillBadge = defineComponent({
  name: "SkillBadge",
  props: { borderColor: String, title: String, textColor: String, points: Array },
  setup(props) {
    return () =>
      h("div", { class: `border-l-4 pl-4 mb-4 ${props.borderColor}` }, [
        h("h3", { class: `font-semibold ${props.textColor}` }, props.title),
        h(
          "ul",
          { class: "text-sm text-gray-600 mt-1" },
          props.points?.map((p, i) => h("li", { key: i }, `• ${p}`))
        ),
      ]);
  },
});

const SessionStat = defineComponent({
  name: "SessionStat",
  props: { label: String, value: Number, color: String },
  setup(props) {
    const map = {
      blue: "bg-blue-100 text-blue-800",
      purple: "bg-purple-100 text-purple-800",
      green: "bg-green-100 text-green-800",
    };
    const colorClasses = computed(() => map[props.color] || "bg-gray-100 text-gray-800");

    return () =>
      h("div", { class: "flex justify-between items-center" }, [
        h("span", { class: "text-sm font-medium" }, props.label),
        h(
          "span",
          { class: `px-3 py-1 rounded-full text-sm font-semibold ${colorClasses.value}` },
          props.value
        ),
      ]);
  },
});

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
  chatHistory.value = [{ role: "assistant", content: greetings[mode], timestamp: new Date() }];
  scrollToBottom();
}

async function sendMessage() {
  if (!userMessage.value.trim() || isThinking.value) return;

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
            "You are in *Assessment Mode*. Your task is to evaluate the user's drafts.\n\n" +
            "Here are the drafts:\n" +
            "Original Draft:\n---\n" +
            `${originalDraft.value || '(empty)'}\n---\n\n` +
            "Final Draft:\n---\n" +
            `${finalDraft.value || '(empty)'}\n---\n\n` +
            "Please provide a critical reflection that:\n" +
            "1. Identifies key differences between the drafts.\n" +
            "2. Highlights specific improvements (clarity, structure, tone, persuasiveness, etc.).\n" +
            "3. Points out remaining weaknesses or areas that could still be enhanced.\n" +
            "4. Offers constructive, actionable suggestions for revision.",
        },
        ...payloadHistory,
      ];
    } else if (currentMode.value === "training") {
      // Insert system message  for backend
      payloadHistory = [
        {
          role: "system",
          content: greetings[currentMode.value],
        },
        ...payloadHistory,
      ];
    }

    const res = await fetch(`${BASE_URL}/chatbot/chat_openrouter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_history: payloadHistory }),
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

function exportChatHistory() {
  const blob = new Blob([JSON.stringify(chatHistory.value, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "chat_history.json";
  a.click();
  URL.revokeObjectURL(url);
}

// ✅ Auto-init
switchMode(currentMode.value);

// API Connection State
const isConnected = ref(false);
const isConnecting = ref(false);
const apiKey = ref("");
const notification = ref({ message: "", type: "success", visible: false });
const model = ref("gpt-5-mini");

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

onMounted(async () => {
  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    await connectAPI(true);
  }
});

</script>
