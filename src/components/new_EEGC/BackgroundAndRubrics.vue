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
                @paste="(e) => handleMarkdownPaste(e, 'course')"
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
        v-if="currentMode == 'training'"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Copy Markdown
      </button>
    </div>
    <p v-if="isCourseInforSubmitted && currentMode == 'training'">
      The Course Information has been submitted. Please note that this is training mode, so the
      information has been pre-filled for your convenience. You will be required to enter it
      manually in assessment mode. Remember to copy the markdown, and use it in assessment mode.
    </p>
    <!-- Student Background -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">🎓 Student Background</h3>
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
                @paste="(e) => handleMarkdownPaste(e, 'student')"
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
        Submit Student Background
      </button>
      <button
        @click="copyStudentContextMarkdown"
        v-if="currentMode == 'training'"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
      >
        Copy Markdown
      </button>
    </div>
    <p v-if="isStudentContextSubmitted && currentMode == 'training'">
      The Student Background has been submitted. Please note that this is training mode, so the
      information has been pre-filled for your convenience. You will be required to enter it
      manually in assessment mode. Remember to copy the markdown, and use it in assessment mode.
    </p>
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
        v-if="currentMode == 'training'"
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
import Swal from "sweetalert2";

const props = defineProps({
  courseInfo: { type: Object, required: true },
  studentContext: { type: Object, required: true },
  rubric: { type: String, default: "" },
  currentMode: { type: String, default: "assessment" },
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

const isCourseInforSubmitted = ref(false);
const isStudentContextSubmitted = ref(false);

/* -------- WATCHERS -------- */
watch(localCourseInfo, (val) => emit("update:courseInfo", { ...val }), { deep: true });
watch(localStudentContext, (val) => emit("update:studentContext", { ...val }), { deep: true });

/* -------- HELPERS -------- */
function formatLabel(key) {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}
function hasEmptyFields(obj) {
  return Object.values(obj).some((val) => !val || !val.trim());
}

/* -------- UNIFIED MARKDOWN PASTE HANDLER -------- */
function handleMarkdownPaste(event, type) {
  const pastedText = (event.clipboardData || window.clipboardData).getData("text");

  const isCourse = pastedText.includes("📘 Course Information");
  const isStudent = pastedText.includes("🎓 Student Background");

  if (!isCourse && type === "course" && !isStudent && type === "student") return;

  const lines = pastedText
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.startsWith("- **"));

  if (!lines.length) return;

  const parsed = {};
  lines.forEach((line) => {
    const m = line.match(/-\s*\*\*([^*]+?)\*\*:?[\s-]*(.+)/);
    if (m) {
      const key = m[1].replace(/[:\s]+/g, "").toLowerCase();
      const value = m[2].trim();
      parsed[key] = value;
    }
  });

  const targetObj = type === "course" ? localCourseInfo : localStudentContext;
  let isTargetFound = false;
  Object.keys(targetObj).forEach((field) => {
    const normalized = field.replace(/\s+/g, "").toLowerCase();
    for (const parsedKey in parsed) {
      if (normalized === parsedKey) {
        isTargetFound = true;
        targetObj[field] = parsed[parsedKey];
      }
    }
  });
  if (!isTargetFound) {
    Swal.fire({
      icon: "error",
      title: "No matching fields found!",
      text: `The pasted markdown did not contain any fields matching the ${
        type === "course" ? "Course Information" : "Student Background"
      } form.`,
    });
  } else {
    Swal.fire({
      icon: "success",
      title: type === "course" ? "Course Information Detected!" : "Student Background Detected!",
      text: "The form fields were filled automatically.",
      timer: 1000,
    });
  }
}

/* -------- SUBMIT HANDLERS -------- */
function handleSubmitCourseInfo() {
  if (hasEmptyFields(localCourseInfo)) {
    return Swal.fire({
      text: "Please fill in all Course Information fields before submitting.",
      icon: "error",
    });
  }
  isCourseInforSubmitted.value = true;
  emit("submitCourseInfo", { ...localCourseInfo });
}
function handleSubmitStudentContext() {
  if (hasEmptyFields(localStudentContext)) {
    return Swal.fire({
      text: "Please fill in all Student Background fields before submitting.",
      icon: "error",
    });
  }
  isStudentContextSubmitted.value = true;
  emit("submitStudentContext", { ...localStudentContext });
}
function handleSubmitRubric() {
  if (!isCourseInforSubmitted.value || !isStudentContextSubmitted.value) {
    return Swal.fire({
      text: "Please submit Course Information and Student Background before submitting the rubric.",
      icon: "error",
    });
  }
  if (!localRubric.value.trim()) {
    return Swal.fire({
      text: "Please provide a rubric before submitting.",
      icon: "error",
    });
  }
  emit("submitRubric", localRubric.value);
}

/* -------- COPY HELPERS -------- */
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    Swal.fire({
      text: "Copied to clipboard as Markdown!",
      icon: "success",
      timer: 1000,
    });
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
  copyToClipboard(`### 🎓 Student Background\n${md}`);
}
function copyRubricMarkdown() {
  copyToClipboard(`### 📊 Rubric\n\n${localRubric.value}`);
}

/* -------- CLEAR ALL -------- */
function handleClearAll() {
  for (const key in localCourseInfo) localCourseInfo[key] = "";
  for (const key in localStudentContext) localStudentContext[key] = "";
  localRubric.value = "";
}
</script>
