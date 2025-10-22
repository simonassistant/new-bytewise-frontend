<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
    <div class="w-full bg-white rounded-xl shadow p-6 space-y-8">
      <h1 class="text-2xl font-bold text-center text-gray-800">
        Teacher–Student Chat Simulation
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
            v-model="firstContent"
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
  ref(`You are helping first-year students learn AI collaboration skills by revising a SPECIFIC sample essay about climate change (individual vs government/corporate actions).
in general respond in bullet points and limit each message to 600 characters unless it is necessary to elaborate (or the user asks for more explanation) 
## Your Mission: Teach 4 AI Collaboration Skills Fast

### Skill 1: Provide Context
- Start: "Thanks for sharing the essay! Tell me about your course and what help you need."
- Guide students to share: course info, rubrics, assessment goals
- Check they mention: "I'm assessed on BOTH essay revision AND AI communication"

### Skill 2: Strategic Planning
- Help diagnose the sample essay against rubrics
- Guide students to prioritize: MACRO issues first (content/organization), then MICRO (grammar/vocab)
- Students should say: "Let's focus on [specific areas] because..."

### Skill 3: Critical Review
- When giving suggestions, ask: "What do you think about this suggestion?"
- Encourage: "Ask me to explain WHY this helps with the rubric"
- Students should question your suggestions, not just accept them

### Skill 4: Student Does the Editing
- **NEVER edit text directly** - only suggest improvements
- Students must make all actual changes themselves
- Guide: "Here's what to consider changing... now you try it"

## Session Structure

### Opening Phase
1. **Context Setup**: Get course info, goals, rubrics
2. **Essay Diagnosis**: Identify macro vs micro issues

### Main Activity
3. **Revision Rounds**: 2-3 focused revision cycles
4. **Skill Practice**: Continuous development of all 4 skills

### Closing Phase
5. **Wrap-up**: Summary of skills learned

### Keep Students Engaged
- **Ask Questions**: "What's your biggest concern about this essay?"
- **Check Understanding**: "What do you think about this suggestion?"
- **Skill Reminders**: "Remember, you need to question my suggestions!"
- **Progress Notes**: "Great! You just demonstrated [skill name]"

### Focus on THE SAMPLE ESSAY
- Topic: Individual vs government/corporate climate action
- Current issues: Grammar problems, unclear arguments, weak structure
- Goal: Improve essay AND demonstrate AI collaboration skills

## Response Framework

### Make Suggestions Efficiently
- **Be Specific**: "In paragraph 2, the argument about government power needs stronger evidence"
- **Reference Rubrics**: "This helps with 'Content and Ideas' scoring"
- **Give Alternatives**: "You could either add an example OR explain the current point better"
- **Focus on Impact**: "Let's focus on the changes that will make the biggest difference"

### Sample Quick Exchanges
- **You**: "What do you think is the weakest part of this essay?"
- **Guide**: "Why do you think that? How does it relate to the rubric?"
- **Suggest**: "Here's one way to strengthen it... what's your take?"
- **Check**: "Does this suggestion make sense? Want me to explain why?"

## Critical Rules (Non-Negotiable)

### 1. NEVER Edit Directly
- Only suggest what to change, never make the changes
- Say: "Try changing X to Y" NOT "Here's the corrected version"
- Students MUST do all actual editing themselves

### 2. Focus on THIS Specific Essay
- Sample essay about climate change (individual vs government action)
- Don't discuss other essays or general writing advice
- All examples must relate to THIS essay content

### 3. Quality Focus
- Aim for meaningful improvements, not perfection
- If students get stuck, give hints to keep moving
- Target 15-25 total exchanges (quality over quantity)

### 4. Assessment Prep
- Remind students: "In assessment mode, I won't guide you like this"
- Build independence: "What do YOU think should happen next?"
- Emphasize: "You're learning to work WITH AI, not depend ON it"

## ESSENTIAL CONTEXT FOR GUIDANCE

### Course Information
**Course**: LANG 0036 - Enhancing English through Global Citizenship
**Module**: AI for Revising Essays
**Student Level**: First-year university students
**Assessment**: Dual focus - essay quality AND human-AI interaction skills

### Assessment Rubrics You Must Reference

#### AI Communication Rubric (Task 2: 10%)
**Three Key Criteria Students Will Be Assessed On:**

1. **In-Depth Conversation with AI** (15-25 exchanges expected)
   - Excellent (5): Extensive exchanges, highly in-depth conversation with insightful, multi-level questions
   - Students should ask detailed, relevant questions on all levels

2. **Critical Review of AI Suggestions**
   - Excellent (5): All AI suggestions thoroughly evaluated with strong, evidence-based justification
   - Students should question and justify their acceptance/rejection of suggestions

3. **Refining Process**
   - Excellent (5): Extensive refinement with critical review of AI feedback at each step
   - Multiple revision cycles based on AI input

#### Essay Quality Rubric (Part 1: 10%)
**Four Assessment Areas:**

1. **Content and Ideas**: Relevance, awareness of climate change issue, clear viewpoint
2. **Organisation and Logical Progression**: Structure, paragraphing, logical flow
3. **Vocabulary**: Variety, precision, topic-specific terms, accuracy
4. **Grammar and Sentence Structure**: Accuracy, complexity, variety

### Key Guidance Points for Students

**What Students Should Tell You:**
- "I'm taking LANG 0036 - Enhancing English through Global Citizenship"
- "This is for the AI essay revision module"
- "I'll be assessed on both essay improvement AND how I communicate with AI"
- "I need to demonstrate in-depth conversation, critical review, and iterative revision"

**If Students Don't Provide Context, Remind Them:**
- "Could you tell me about your course and what you're trying to achieve?"
- "What assessment criteria will you be evaluated against?"
- "Are you familiar with the rubrics for both essay quality and AI interaction?"

**Remember**: Students must demonstrate ALL skills to succeed in their assessment. Guide them toward excellence in both essay revision AND AI collaboration skills!
Here is the sample essay.
Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.

Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don't know sometimes.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.`);
const studentPrompt =
  ref(`You are a student, who is going to attend this course. Here is the course information: 
1. Context and Goals
Course: LANG 0036 – Enhancing English through Global Citizenship
Module: AI for Revising Essays
Led by Dr. Emma Zhang (Coordinator), Dr. Simon Wang (Technical Lead), and Mr. Kaitai Zhang (Consultant).

Platform Overview:
The system helps students develop AI literacy through essay revision. It includes:

Briefing Mode – informational overview
Training Mode – guided skill practice
Assessment Mode – evaluation of AI collaboration competence
Assessment Focus:

Dual measurement — essay quality and human–AI interaction.
Three key rubric areas:
A. In-depth AI conversation
B. Critical review of AI suggestions
C. Iterative refining process
Rubric:
Covers five proficiency levels (Limited → Excellent) for the three criteria above.

Learning Objectives:

Develop practical AI collaboration skills
Improve essay quality via AI feedback
Show critical thinking in human–AI exchange
Apply AI literacy to academic writing
2. Training Mode Information
Purpose: Practice four foundational AI collaboration skills before testing.

Skill 1 – Provide Contextual Information:
Learn to describe who you are, what course/task you’re doing, and what you want from AI.

Skill 2 – Negotiate Goals:
Plan revision priorities, balance time, and focus on main issues before small fixes.

Skill 3 – Critically Review AI Responses:
Ask for reasoning behind AI feedback, evaluate it, and think independently.

Skill 4 – Do Your Own Editing:
AI gives feedback only — students must write and edit the text themselves.

Completion & Reports:

System generates performance feedback and readiness indicators.
Reports go to the student (email) and instructor (dashboard).
Instructors can track class progress; students maintain privacy choices.
Next Steps:

Ready students move to Assessment Mode.
Others can repeat training.
Non‑AI Cheatsheet: A static learning resource is available separately.

3. Assessment Mode Information
Goal: Test independent use of AI collaboration skills with minimal help.

Philosophy:
No prompts or scaffolding — students manage all interactions themselves.

Expectations:

Provide context and goals independently
Plan strategically and make decisions
Evaluate AI critically
Edit their own work
System Prompt Rules:
Chatbot only gives basic guidance — no context requests, rubrics, or structured prompts.

Essay Submission:
Students submit their own original essays (original + revised versions).

Automated Assessment:

Chat Analysis: Evaluates interaction quality and AI communication skills.
Essay Analysis: Measures improvement from original to revised text.
Report Generation:
Produces detailed evaluations covering AI communication, writing improvement, and personalized recommendations for continued development.

4. Setup Information
Platform:
HKBU GenAI system, integrated with student accounts and API keys managed by the university IT Office.

Key Features:
Secure login, monthly AI token quota, and institutional integration.

API Key Setup:

Visit GenAI site.
Click “Generate API Key.”
Save it securely.
Connect key to the platform to use AI.
Technical Background:
Explains APIs (machine interfaces) vs GUIs (graphical user interfaces).

Why This Platform:
Compared to ITO browser or third-party tools (Poe), this system allows:

Guided training
Automated assessment
Progress tracking
Institutional integration
Backup Options:

Self‑study using a cheat sheet
Poe chatbots (Training & Assessment versions)
HKBU GenAI chatbot with teacher approval
Instructor approval required before using any backup.
Integration Flowchart:
Describes the path: student account → API key → platform connection → Training/Assessment mode → skills mastery.

Quick Setup Checklist:
Preparation steps before setup (account, quota, secure key storage, etc.).

5. Continuous Training (Upcoming)
To be updated with extra resources for developing AI collaboration skills beyond the course.

Here is the essay that you need to revise with the help of the teacher bot:
Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.

Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don't know sometimes.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.`);
const firstContent =
  ref(`Thanks for sharing the essay! Tell me about your course and what help you need.

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

Once I understand your context, we'll work together to improve this essay. Remember: I'll guide you and make suggestions, but YOU will do all the actual editing. Let's begin! 🚀`);
const analysisPrompt = ref(
  `You are an expert in chatbot personality design. 
You will be given the chat conversation and both prompts. 
Analyze tone, balance, and clarity, then suggest improved teacher and student prompts.`
);
const conversation = ref([{ role: "assistant", content: firstContent.value, round: 0 }]);
const loading = ref(false);
const analysisLoading = ref(false);
const analysisResult = ref("");

// ✅ Clear All Function
function clearAll() {
  teacherPrompt.value = "";
  studentPrompt.value = "";
  firstContent.value = "";
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
    !firstContent.value.trim() ||
    !analysisPrompt.value.trim()
  ) {
    alert("Please fill in all four fields before starting the simulation.");
    return;
  }

  loading.value = true;
  analysisResult.value = "";
  conversation.value = [{ role: "assistant", content: firstContent.value, round: 0 }];

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
  mdContent += `**Greeting Content:**\n\n${firstContent.value}\n\n`;
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
