<template>
  <div class="bg-white text-gray-900 transition-colors duration-300 min-h-screen">
    <div class="container mx-auto max-w-6xl p-4">
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
              currentMode === 'training' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            "
          >
            {{ currentMode === "training" ? "Training Mode Active" : "Assessment Mode Active" }}
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <div
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
              students had discovered many side of zoom. They use zoom to take tutorial classes, have
              meeting with group mates and so on. Internet not only allow students to study at home, but
              also provide a new learning style. Apart from that, the internet is also contributes to
              our health. With the rapid development of the 5G technology, doctors are able to operate
              more precisely Robot-Assist surgery (RAs). This means we can have less trauma, less covery
              time and better surgery effect. And it all thanks to the high speed and stable internet.
              Some people may worried about their privacy issue while using the internet. However, in my
              opinion, as long as we pay more attention to our behaviour such as not viewing strange
              website, not giving out our personal information and so on. We can protect our privacy to
              a certain extent. (170 words)"
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h, defineComponent } from "vue";

/* ------------ State ------------ */
const currentMode = ref("training");
const stats = ref({
  exchanges: 0,
  questions: 0,
  revisions: 0,
});
const originalDraft = ref("");
const finalDraft = ref("");

const activeBtn =
  "px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:opacity-90 transition-opacity";
const inactiveBtn =
  "px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:opacity-90 transition-opacity";

/* ------------ Components ------------ */
const SkillBadge = defineComponent({
  name: "SkillBadge",
  props: {
    borderColor: String,
    title: String,
    textColor: String,
    points: Array,
  },
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
  props: {
    label: String,
    value: Number,
    color: String,
  },
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

/* ------------ Methods ------------ */
function switchMode(mode) {
  currentMode.value = mode;
  stats.value = { exchanges: 0, questions: 0, revisions: 0 };
}

function exportChatHistory() {
  alert("No conversation history to export yet.");
}
</script>
