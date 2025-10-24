<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
    <div class="w-full bg-white rounded-xl shadow p-6 space-y-8">
      <h1 class="text-2xl font-bold text-center text-gray-800">
        Teacher–Student Chat Simulation 1.01
      </h1>

      <!-- Prompt Inputs -->
      <div class="space-y-4">
        <div>
          <label class="block font-semibold mb-1 text-gray-700">Teacher Prompt</label>
          <textarea
            v-model="teacherPrompt"
            rows="10"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter teacher prompt..."
          ></textarea>
        </div>

        <div>
          <label class="block font-semibold mb-1 text-gray-700">Student Prompt</label>
          <textarea
            v-model="studentPrompt"
            rows="10"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter student prompt..."
          ></textarea>
        </div>

        <div>
          <label class="block font-semibold mb-1 text-gray-700">Greeting Content</label>
          <textarea
            v-model="greetingContent"
            rows="10"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter initial message..."
          ></textarea>
        </div>

        <div>
          <label class="block font-semibold mb-1 text-gray-700">Analysis Prompt</label>
          <textarea
            v-model="analysisPrompt"
            rows="4"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter analysis instructions..."
          ></textarea>
        </div>
      </div>

      <!-- Options -->
      <div
        class="flex flex-wrap items-center justify-between border-t pt-4 mt-6 space-y-3 sm:space-y-0"
      >
        <div class="flex items-center space-x-2">
          <label class="font-semibold text-gray-700">Auto Scroll:</label>
          <input
            type="checkbox"
            v-model="autoScroll"
            class="h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
        </div>

        <div class="flex items-center space-x-2">
          <label class="font-semibold text-gray-700">Chat Rounds:</label>
          <input
            type="number"
            v-model.number="chatRounds"
            min="1"
            max="1000"
            class="w-20 border rounded-lg p-1 text-center focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-center space-x-4 mt-4">
        <button
          @click="startSimulation"
          :disabled="loading || analysisLoading"
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4 py-2 rounded-lg disabled:opacity-50"
        >
          {{ loading ? "Running..." : "Start Chat Simulation" }}
        </button>

        <button
          @click="clearAll"
          class="bg-red-500 hover:bg-red-600 text-white font-medium px-4 py-2 rounded-lg"
        >
          Clear All
        </button>

        <!-- ✅ Download Markdown Button -->
        <button
          @click="downloadMarkdown"
          class="bg-green-600 hover:bg-green-700 text-white font-medium px-4 py-2 rounded-lg"
        >
          Download Markdown
        </button>
      </div>

      <!-- Chat -->
      <div v-if="conversation.length" class="border-t pt-6 space-y-4">
        <h2 class="text-xl font-semibold">Chat Conversation</h2>
        <div class="space-y-3" ref="chatContainer">
          <div v-for="(msg, idx) in conversation" :key="idx" class="my-3">
            <div
              :class="[
                'p-7 rounded-lg shadow-sm border relative',
                msg.role === 'assistant'
                  ? 'bg-blue-50 border-blue-200 text-blue-800'
                  : 'bg-purple-50 border-purple-200 text-purple-800',
              ]"
            >
              <div
                class="absolute -top-3 left-3 bg-gray-200 text-gray-700 text-xs px-2 py-0.5 rounded-full shadow-sm"
              >
                Round {{ msg.round }}
              </div>

              <span class="font-semibold block mb-1">
                {{ msg.role === "assistant" ? "Teacher" : "Student" }}:
              </span>

              <div
                class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
                v-html="renderMarkdown(msg.content)"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis Output -->
      <div v-if="analysisLoading || analysisResult" class="border-t pt-6">
        <h2 class="text-xl font-semibold">Analysis Result</h2>

        <div v-if="analysisLoading" class="text-gray-500 italic">Analyzing conversation...</div>

        <div
          v-else
          class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
          v-html="renderMarkdown(analysisResult)"
        ></div>
      </div>
    </div>
    <div ref="scrollAnchor"></div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { BASE_URL } from "@/components/base_url";
import MarkdownIt from "markdown-it";

const markdown = new MarkdownIt({ html: false, linkify: true, typographer: true });
const renderMarkdown = (text) => markdown.render(text || "");

// DOM Refs
const scrollAnchor = ref(null);
const chatContainer = ref(null);

// Options
const autoScroll = ref(true);
const chatRounds = ref(20);

// State Variables
const teacherPrompt =
  ref(`You are an experienced language teacher with expertise and passion for helping first-year students revise their essays, focusing specifically on thesis statements. Begin the conversation with this friendly greeting:
'''
Hi, please share your practice essay for revision.
'''
Your role is to engage the student interactively by providing clear, supportive, and actionable hints and suggestions on how to improve the thesis statement of their essay. Throughout the conversation:

Listen carefully to the student’s thesis and offer constructive feedback using specific revision tips.
Encourage the student to try revising their thesis themselves, but offer to help rewrite it if they ask.
Suggest ways to make their thesis clearer, stronger, more concise, and confident.
Remind them to avoid vague or weak language (e.g., “I think,” “I guess”) and to clearly indicate their main argument and the key points they will explore.
Provide examples of improved thesis statements as models for their revision.
Keep the tone encouraging, patient, and student-centered.
Prompt the student periodically if they have further questions or want to continue revising the thesis. If the student types “done,” politely conclude the chat by acknowledging their work and encouraging them to reach out in the future for help with other parts of their essay. End the conversation gracefully.

Your entire focus should remain on revising the thesis statement only—do not discuss other parts of the essay. Maintain an interactive and supportive environment that helps the student gain confidence and skills in crafting strong thesis statements.`);
const studentPrompt =
  ref(`You are a student taking the Course: LANG 0036 – Enhancing English through Global Citizenship led by Dr. Emma Zhang (Coordinator), Dr. Simon Wang (Technical Lead), and Mr. Kaitai Zhang (Consultant). You will receive a greeting message as follows 
'''
Hi please share your practice essay for revision. 

'''
you should then share the essay as follows 
'''
Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.


First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don’t hurt environment. This is good because it change many people life at once. So powerful, you know.


But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don’t always do it. Also, one person doing something. It not enough.


Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.


Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don’t know sometimes.


Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That’s my opinion.
''


The teacher will provide you instructions and feedback on how to revise. The focus is on revising the thesis statement.  You should take the teacher's advice on how to revise the thesis statement and only try to revise the thesis statement but NOTHING Else. You should type "done" and end the chat when you finish revising the thesis statement and have no further question. 

Reminder: you are the student and you should be revising the essay. `);
const greetingContent = ref(`Hi please share your practice essay for revision. `);
const analysisPrompt = ref(
  `You are an expert in chatbot personality design. You will be given the chat history and both prompts. 
Your job is to analyze the overall usefulness of the bot for the student and identify areas where the student and the teacher might improve. `
);
const conversation = ref([{ role: "assistant", content: greetingContent.value, round: 0 }]);
const loading = ref(false);
const analysisLoading = ref(false);
const analysisResult = ref("");

// ✅ Clear All Function
function clearAll() {
  teacherPrompt.value = "";
  studentPrompt.value = "";
  greetingContent.value = "";
  analysisPrompt.value = "";
  conversation.value = [];
  analysisResult.value = "";
}

// Helper: Scroll chat view
async function scrollToBottom() {
  await nextTick();
  if (autoScroll.value && scrollAnchor.value) {
    scrollAnchor.value.scrollIntoView({ behavior: "smooth" });
  }
}

// Helper: Send chat to API
async function sendChat(chat_history) {
  try {
    const providerUrl = `${BASE_URL}/chatbot/chat_openrouter`;
    const res = await fetch(providerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_history }),
    });
    const data = await res.json();
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";
    return reply;
  } catch (err) {
    console.error("Chat error:", err);
    return "Error connecting to chat endpoint.";
  }
}

// ✅ Main Simulation Logic
async function startSimulation() {
  if (
    !teacherPrompt.value.trim() ||
    !studentPrompt.value.trim() ||
    !greetingContent.value.trim() ||
    !analysisPrompt.value.trim()
  ) {
    alert("Please fill in all four fields before starting the simulation.");
    return;
  }

  loading.value = true;
  analysisResult.value = "";
  conversation.value = [{ role: "assistant", content: greetingContent.value, round: 0 }];

  for (let turn = 0; turn < chatRounds.value; turn++) {
    const isTeacherTurn = turn % 2 === 1;
    const systemPrompt = isTeacherTurn ? teacherPrompt.value : studentPrompt.value;

    const placeholder = {
      role: isTeacherTurn ? "assistant" : "user",
      content: isTeacherTurn ? "_Teacher is thinking..._" : "_Student is thinking..._",
      round: turn + 1,
    };
    conversation.value.push(placeholder);
    await scrollToBottom();

    const convoForModel = JSON.parse(JSON.stringify(conversation.value));
    if (!isTeacherTurn) {
      convoForModel.forEach((msg) => {
        msg.role = msg.role === "assistant" ? "user" : msg.role === "user" ? "assistant" : msg.role;
      });
    }

    const messages = [{ role: "system", content: systemPrompt }, ...convoForModel.slice(0, -1)];
    console.log(messages);
    const reply = await sendChat(messages);

    conversation.value[conversation.value.length - 1].content = reply.trim();
    await scrollToBottom();
    if (reply.trim() == "done") {
      break;
    }
  }

  loading.value = false;
  await analyzePrompts();
}

// Analysis
async function analyzePrompts() {
  if (!conversation.value.length) return;
  analysisLoading.value = true;
  analysisResult.value = "";

  const processedConvo = conversation.value.map((msg) => ({
    ...msg,
    role: msg.role === "assistant" ? "teacher" : "student",
  }));

  const messages = [
    { role: "system", content: analysisPrompt.value },
    {
      role: "user",
      content: JSON.stringify(
        {
          teacher_prompt: teacherPrompt.value,
          student_prompt: studentPrompt.value,
          chat_conversation: processedConvo,
        },
        null,
        2
      ),
    },
  ];

  const reply = await sendChat(messages);
  analysisResult.value = reply.trim();
  analysisLoading.value = false;
  await scrollToBottom();
}

// ✅ Download Markdown Function
function downloadMarkdown() {
  let mdContent = `# Teacher–Student Chat Simulation Export\n\n`;

  mdContent += `## Prompts\n`;
  mdContent += `**Teacher Prompt:**\n\n${teacherPrompt.value}\n\n`;
  mdContent += `**Student Prompt:**\n\n${studentPrompt.value}\n\n`;
  mdContent += `**Greeting Content:**\n\n${greetingContent.value}\n\n`;
  mdContent += `**Analysis Prompt:**\n\n${analysisPrompt.value}\n\n`;

  mdContent += `## Chat Rounds: ${chatRounds.value}\n\n`;
  mdContent += `## Conversation\n`;

  for (const msg of conversation.value) {
    const speaker = msg.role === "assistant" ? "Teacher" : "Student";
    mdContent += `### Round ${msg.round} (${speaker})\n${msg.content}\n\n`;
  }

  if (analysisResult.value) {
    mdContent += `## Analysis Result\n\n${analysisResult.value}\n`;
  }

  const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Teacher-Student-Chat-Export.md";
  a.click();
  URL.revokeObjectURL(url);
}
</script>
