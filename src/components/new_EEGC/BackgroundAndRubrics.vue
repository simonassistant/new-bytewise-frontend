<template>
  <div class="p-4 bg-gray-50 rounded-lg mb-6">
    <h2 class="text-xl font-bold text-gray-900 mb-4 text-center">📝 Course & Student Background</h2>

    <!-- Course Information -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">📘 Course Information</h3>
    
    <!-- Info Alert about AI Sharing -->
    <div class="mb-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
      <p class="text-sm text-blue-900">
        <strong>ℹ️ Important:</strong> This course information will be shared with the AI tutor so it can provide contextually relevant feedback and guidance based on your course requirements.
      </p>
    </div>

    <!-- Course Info Container -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
      <h4 class="text-md font-semibold text-gray-700 mb-3">
        {{ isCourseInforSubmitted ? "📋 Course Information (Read-only)" : "📋 Course Information" }}
      </h4>

      <!-- Tabs for Edit/Preview -->
      <div v-if="!isCourseInforSubmitted" class="mb-3 border-b border-gray-200">
        <button
          @click="courseInfoTab = 'edit'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            courseInfoTab === 'edit' 
              ? 'border-blue-600 text-blue-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Edit
        </button>
        <button
          @click="courseInfoTab = 'preview'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            courseInfoTab === 'preview' 
              ? 'border-blue-600 text-blue-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Preview
        </button>
      </div>

      <!-- Edit Tab -->
      <div v-if="!isCourseInforSubmitted && courseInfoTab === 'edit'" class="mb-4">
        <div class="overflow-x-auto">
          <table class="w-full text-sm border border-gray-200 rounded-lg">
            <tbody>
              <tr
                v-for="(value, key) in localCourseInfo"
                :key="key"
                class="even:bg-gray-50 border-b border-gray-200"
              >
                <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700 bg-gray-100">
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
      </div>

      <!-- Preview Tab (before submission) -->
      <div v-if="!isCourseInforSubmitted && courseInfoTab === 'preview'" class="mb-4">
        <!-- Explanation about Machine-Readable Codes -->
        <div class="mb-3 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <p class="text-sm text-yellow-900">
            <strong>💡 Reminder:</strong> AI tutors prefer machine-readable codes. Please copy the markdown code below and paste it into assessment mode when needed.
          </p>
        </div>
        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50 overflow-x-auto">
          <div 
            class="preview-content"
            v-html="renderedCourseInfo"
          ></div>
        </div>
        <div class="mt-3 flex justify-end">
          <button
            @click="copyCourseInfoMarkdown"
            class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium px-3 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          >
            📋 Copy Markdown
          </button>
        </div>
      </div>

      <!-- Read-only view (after submission) -->
      <div v-if="isCourseInforSubmitted" class="mb-4">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border border-gray-200 rounded-lg">
            <tbody>
              <tr
                v-for="(value, key) in localCourseInfo"
                :key="key"
                class="even:bg-gray-50 border-b border-gray-200"
              >
                <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700 bg-gray-100">
                  {{ formatLabel(key) }}
                </th>
                <td class="px-4 py-2">
                  <div class="text-gray-900 py-2 px-1 bg-gray-50 rounded border border-gray-200">
                    {{ value || "—" }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Markdown Code Display (after submission) -->
        <div class="mb-3 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <p class="text-sm text-yellow-900">
            <strong>💡 Reminder:</strong> AI tutors prefer machine-readable codes. Please copy the markdown code below and paste it into assessment mode when needed.
          </p>
        </div>
        <div class="bg-gray-900 rounded-lg p-4">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-md font-semibold text-gray-200">📝 Markdown Code (Copy for Assessment Mode)</h4>
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

      <!-- Submit Button (only before submission) -->
      <div v-if="!isCourseInforSubmitted" class="flex justify-center gap-3 mt-4">
        <button
          @click="handleSubmitCourseInfo"
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 transition"
        >
          Submit Course Info
        </button>
      </div>
    </div>

    <!-- Student Context -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">🎓 Student Context</h3>

    <!-- Student Context Container -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
      <h4 class="text-md font-semibold text-gray-700 mb-3">
        {{ isStudentContextSubmitted ? "🎓 Student Context (Read-only)" : "🎓 Student Context" }}
      </h4>

      <!-- Tabs for Edit/Preview -->
      <div v-if="!isStudentContextSubmitted" class="mb-3 border-b border-gray-200">
        <button
          @click="studentContextTab = 'edit'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            studentContextTab === 'edit' 
              ? 'border-green-600 text-green-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Edit
        </button>
        <button
          @click="studentContextTab = 'preview'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            studentContextTab === 'preview' 
              ? 'border-green-600 text-green-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Preview
        </button>
      </div>

      <!-- Edit Tab -->
      <div v-if="!isStudentContextSubmitted && studentContextTab === 'edit'" class="mb-4">
        <div class="overflow-x-auto">
          <table class="w-full text-sm border border-gray-200 rounded-lg">
            <tbody>
              <tr
                v-for="(value, key) in localStudentContext"
                :key="key"
                class="even:bg-gray-50 border-b border-gray-200"
              >
                <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700 bg-gray-100">
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
      </div>

      <!-- Preview Tab (before submission) -->
      <div v-if="!isStudentContextSubmitted && studentContextTab === 'preview'" class="mb-4">
        <!-- Explanation about Machine-Readable Codes -->
        <div class="mb-3 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <p class="text-sm text-yellow-900">
            <strong>💡 Reminder:</strong> AI tutors prefer machine-readable codes. Please copy the markdown code below and paste it into assessment mode when needed.
          </p>
        </div>
        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50 overflow-x-auto">
          <div 
            class="preview-content"
            v-html="renderedStudentContext"
          ></div>
        </div>
        <div class="mt-3 flex justify-end">
          <button
            @click="copyStudentContextMarkdown"
            class="bg-green-600 hover:bg-green-700 text-white text-xs font-medium px-3 py-1 rounded focus:outline-none focus:ring-2 focus:ring-green-400 transition"
          >
            📋 Copy Markdown
          </button>
        </div>
      </div>

      <!-- Read-only view (after submission) -->
      <div v-if="isStudentContextSubmitted" class="mb-4">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border border-gray-200 rounded-lg">
            <tbody>
              <tr
                v-for="(value, key) in localStudentContext"
                :key="key"
                class="even:bg-gray-50 border-b border-gray-200"
              >
                <th class="text-left px-4 py-2 w-1/3 font-semibold text-gray-700 bg-gray-100">
                  {{ formatLabel(key) }}
                </th>
                <td class="px-4 py-2">
                  <div class="text-gray-900 py-2 px-1 bg-gray-50 rounded border border-gray-200">
                    {{ value || "—" }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Markdown Code Display (after submission) -->
        <div class="mb-3 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <p class="text-sm text-yellow-900">
            <strong>💡 Reminder:</strong> AI tutors prefer machine-readable codes. Please copy the markdown code below and paste it into assessment mode when needed.
          </p>
        </div>
        <div class="bg-gray-900 rounded-lg p-4">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-md font-semibold text-gray-200">📝 Markdown Code (Copy for Assessment Mode)</h4>
            <button
              @click="copyStudentContextMarkdown"
              class="bg-green-600 hover:bg-green-700 text-white text-xs font-medium px-3 py-1 rounded focus:outline-none focus:ring-2 focus:ring-green-400 transition"
            >
              📋 Copy
            </button>
          </div>
          <pre class="text-xs text-green-400 overflow-x-auto whitespace-pre-wrap"><code>{{ getStudentContextMarkdown() }}</code></pre>
        </div>
      </div>

      <!-- Submit Button (only before submission) -->
      <div v-if="!isStudentContextSubmitted" class="flex justify-center gap-3 mt-4">
        <button
          @click="handleSubmitStudentContext"
          class="bg-green-600 hover:bg-green-700 text-white font-medium px-4 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 transition"
        >
          Submit Student Context
        </button>
      </div>
    </div>

    <!-- Rubrics Input -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
      <h3 class="font-semibold text-gray-900 mb-2">📊 Rubrics Input</h3>
      
      <!-- Tabs for Edit/Preview -->
      <div class="mb-3 border-b border-gray-200">
        <button
          @click="rubricTab = 'edit'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            rubricTab === 'edit' 
              ? 'border-purple-600 text-purple-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Edit
        </button>
        <button
          @click="rubricTab = 'preview'"
          :class="[
            'px-4 py-2 text-sm font-medium border-b-2 transition',
            rubricTab === 'preview' 
              ? 'border-purple-600 text-purple-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Preview
        </button>
      </div>

      <!-- Edit Tab -->
      <div v-if="rubricTab === 'edit'" class="mb-4">
        <textarea
          v-model="localRubric"
          placeholder="Paste or type your rubric here..."
          rows="12"
          class="w-full border border-gray-300 rounded-lg p-2 text-sm font-mono focus:outline-none focus:ring focus:ring-indigo-300"
        ></textarea>
      </div>

      <!-- Preview Tab -->
      <div v-else class="mb-4">
        <div 
          class="border border-gray-200 rounded-lg p-4 bg-gray-50 overflow-x-auto rubric-preview"
          v-html="renderedRubric"
        ></div>
      </div>

      <div class="flex justify-center gap-3">
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
import { reactive, ref, watch, computed } from "vue";
import MarkdownIt from "markdown-it";
const isCourseInforSubmitted = ref(false);
const isStudentContextSubmitted = ref(false);
const rubricTab = ref("edit");
const courseInfoTab = ref("edit");
const studentContextTab = ref("edit");
import Swal from "sweetalert2";

// Initialize markdown renderer
const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
});

// Render rubric as HTML
const renderedRubric = computed(() => {
  if (!localRubric.value) return "<p class='text-gray-400'>No rubric content to preview</p>";
  return md.render(localRubric.value);
});

// Render course info as HTML
const renderedCourseInfo = computed(() => {
  return md.render(getCourseInfoMarkdown());
});

// Render student context as HTML
const renderedStudentContext = computed(() => {
  return md.render(getStudentContextMarkdown());
});

const props = defineProps({
  courseInfo: { type: Object, required: true },
  studentContext: { type: Object, required: true },
  rubric: { type: String, default: "" },
  currentMode: { type: String, default: "" },
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

/** Watch for reactive updates (only when not submitted) */
watch(localCourseInfo, (val) => {
  if (!isCourseInforSubmitted.value) {
    emit("update:courseInfo", { ...val });
  }
}, { deep: true });

watch(localStudentContext, (val) => {
  if (!isStudentContextSubmitted.value) {
    emit("update:studentContext", { ...val });
  }
}, { deep: true });

/** Watch for prop changes to sync local state */
watch(() => props.courseInfo, (newVal) => {
  if (newVal && !isCourseInforSubmitted.value) {
    Object.assign(localCourseInfo, newVal);
  }
}, { deep: true });

watch(() => props.studentContext, (newVal) => {
  if (newVal && !isStudentContextSubmitted.value) {
    Object.assign(localStudentContext, newVal);
  }
}, { deep: true });

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
    Swal.fire({
      text: "Copied to clipboard as Markdown!",
      icon: "success",
    });
  });
}
function getCourseInfoMarkdown() {
  const md = Object.entries(localCourseInfo)
    .map(([k, v]) => `- **${formatLabel(k)}:** ${v || "—"}`)
    .join("\n");
  return `### 📘 Course Information\n\n${md}`;
}

function getStudentContextMarkdown() {
  const md = Object.entries(localStudentContext)
    .map(([k, v]) => `- **${formatLabel(k)}:** ${v || "—"}`)
    .join("\n");
  return `### 🎓 Student Context\n\n${md}`;
}

function copyCourseInfoMarkdown() {
  copyToClipboard(getCourseInfoMarkdown());
}
function copyStudentContextMarkdown() {
  copyToClipboard(getStudentContextMarkdown());
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

<style scoped>
.rubric-preview :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.875rem;
}

.rubric-preview :deep(table thead) {
  background-color: #f3f4f6;
}

.rubric-preview :deep(table th) {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border: 1px solid #d1d5db;
  background-color: #f9fafb;
}

.rubric-preview :deep(table td) {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  vertical-align: top;
}

.rubric-preview :deep(table tr:nth-child(even)) {
  background-color: #f9fafb;
}

.rubric-preview :deep(table tr:hover) {
  background-color: #f3f4f6;
}

.rubric-preview :deep(h2) {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.rubric-preview :deep(h3) {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.25rem;
  margin-bottom: 0.75rem;
}

.rubric-preview :deep(h4) {
  font-size: 1.125rem;
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.rubric-preview :deep(p) {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

.rubric-preview :deep(hr) {
  margin: 1.5rem 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}

.preview-content :deep(ul) {
  list-style-type: disc;
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}

.preview-content :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.preview-content :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.75rem;
}
</style>
