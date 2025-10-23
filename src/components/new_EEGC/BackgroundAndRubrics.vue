<template>
  <div class="p-4 bg-gray-50 rounded-lg mb-6">
    <h2 class="text-xl font-bold text-gray-900 mb-4 text-center">📝 Course & Student Background</h2>

    <!-- Course Information -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">📘 Course Information</h3>
    <div class="overflow-x-auto mb-4">
      <table class="w-full text-sm border border-gray-300 rounded-lg">
        <tbody>
          <tr
            v-for="(value, key) in localCourseInfo"
            :key="key"
            class="even:bg-gray-50 border-b border-gray-200"
          >
            <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700">
              {{ formatLabel(key) }}
            </th>
            <td class="px-4 py-2">
              <input
                v-model="localCourseInfo[key]"
                type="text"
                :placeholder="`Enter ${formatLabel(key)}...`"
                class="w-full border border-gray-300 rounded-lg px-2 py-1 focus:outline-none focus:ring focus:ring-indigo-300"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="flex justify-center gap-3 mb-8">
      <button
        @click="handleSubmitCourseInfo"
        :disabled="isCourseInforSubmitted"
        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:text-gray-200 text-white font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 transition"
      >
        Submit Course Info
      </button>
      <button
        @click="copyCourseInfoMarkdown"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Copy Markdown
      </button>
    </div>

    <!-- Student Context -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">🎓 Student Context</h3>
    <div class="overflow-x-auto mb-4">
      <table class="w-full text-sm border border-gray-300 rounded-lg">
        <tbody>
          <tr
            v-for="(value, key) in localStudentContext"
            :key="key"
            class="even:bg-gray-50 border-b border-gray-200"
          >
            <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700">
              {{ formatLabel(key) }}
            </th>
            <td class="px-4 py-2">
              <input
                v-model="localStudentContext[key]"
                type="text"
                :placeholder="`Enter ${formatLabel(key)}...`"
                class="w-full border border-gray-300 rounded-lg px-2 py-1 focus:outline-none focus:ring focus:ring-indigo-300"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="flex justify-center gap-3 mb-8">
      <button
        @click="handleSubmitStudentContext"
        :disabled="isStudentContextSubmitted"
        class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 disabled:text-gray-200 text-white font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 transition"
      >
        Submit Student Context
      </button>
      <button
        @click="copyStudentContextMarkdown"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Copy Markdown
      </button>
    </div>

    <!-- Rubrics Input -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
      <h3 class="font-semibold text-gray-900 mb-2">📊 Rubrics Input</h3>
      <textarea
        v-model="localRubric"
        placeholder="Paste or type your rubric here..."
        rows="6"
        class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring focus:ring-indigo-300"
      ></textarea>
    </div>
    <div class="flex justify-center gap-3 mb-8">
      <button
        @click="handleSubmitRubric"
        class="bg-purple-600 hover:bg-purple-700 text-white font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 transition"
      >
        Submit Rubric
      </button>
      <button
        @click="copyRubricMarkdown"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Copy Markdown
      </button>
    </div>

    <!-- Global Clear Button -->
    <div class="flex justify-center gap-4">
      <button
        @click="handleClearAll"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-6 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Clear All
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from "vue";
const isCourseInforSubmitted = ref(false);
const isStudentContextSubmitted = ref(false);
import Swal from "sweetalert2";

const props = defineProps({
  courseInfo: { type: Object, required: true },
  studentContext: { type: Object, required: true },
  rubric: { type: String, default: "" },
});

const emit = defineEmits([
  "submitCourseInfo",
  "submitStudentContext",
  "submitRubric",
  "update:courseInfo",
  "update:studentContext",
]);

const localCourseInfo = reactive({ ...props.courseInfo });
const localStudentContext = reactive({ ...props.studentContext });
const localRubric = ref(props.rubric || "");

/** Watch for reactive updates */
watch(localCourseInfo, (val) => emit("update:courseInfo", { ...val }), { deep: true });
watch(localStudentContext, (val) => emit("update:studentContext", { ...val }), { deep: true });

/** Helpers */
function formatLabel(key) {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}
function hasEmptyFields(obj) {
  return Object.values(obj).some((val) => !val || !val.trim());
}

/** Submit handlers */
function handleSubmitCourseInfo() {
  if (hasEmptyFields(localCourseInfo)) {
    Swal.fire({
      text: "Please fill in all Course Information fields before submitting.",
      icon: "error",
    });
    return;
  }
  isCourseInforSubmitted.value = true;
  emit("submitCourseInfo", { ...localCourseInfo });
}

function handleSubmitStudentContext() {
  if (hasEmptyFields(localStudentContext)) {
    Swal.fire({
      text: "Please fill in all Student Context fields before submitting.",
      icon: "error",
    });
    return;
  }
  isStudentContextSubmitted.value = true;
  emit("submitStudentContext", { ...localStudentContext });
}

function handleSubmitRubric() {
  if (!isCourseInforSubmitted.value || !isStudentContextSubmitted.value) {
    Swal.fire({
      text: "Please submit Course Information and Student Context before submitting the rubric.",
      icon: "error",
    });
    return;
  }
  if (!localRubric.value.trim()) {
    Swal.fire({
      text: "Please provide a rubric before submitting.",
      icon: "error",
    });
    return;
  }
  emit("submitRubric", localRubric.value);
}

/** Copy Helpers */
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("Copied to clipboard as Markdown!");
  });
}
function copyCourseInfoMarkdown() {
  const md = Object.entries(localCourseInfo)
    .map(([k, v]) => `- **${formatLabel(k)}:** ${v}`)
    .join("\n");
  copyToClipboard(`### 📘 Course Information\n${md}`);
}
function copyStudentContextMarkdown() {
  const md = Object.entries(localStudentContext)
    .map(([k, v]) => `- **${formatLabel(k)}:** ${v}`)
    .join("\n");
  copyToClipboard(`### 🎓 Student Context\n${md}`);
}
function copyRubricMarkdown() {
  copyToClipboard(`### 📊 Rubric\n\n${localRubric.value}`);
}

/** Clear all */
function handleClearAll() {
  for (const key in localCourseInfo) localCourseInfo[key] = "";
  for (const key in localStudentContext) localStudentContext[key] = "";
  localRubric.value = "";
}
</script>
