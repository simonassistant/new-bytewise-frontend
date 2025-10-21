<template>
  <div class="bg-gray-50 dark:bg-[#181818] text-gray-900 dark:text-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-6 max-w-7xl">
      <!-- Header -->
      <header class="mb-6 text-center">
        <h1 class="text-3xl md:text-4xl font-bold text-indigo-600 mb-2">
          Context Confirmation
        </h1>
        <p class="text-base md:text-lg text-gray-600 dark:text-gray-400">
          Goal 1: Provide Contextual Information
        </p>
      </header>

      <div class="space-y-6">
        <!-- Objective 1 -->
        <section
          class="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border-l-4 border-red-500 rounded-lg p-6"
        >
          <div class="flex items-center mb-4">
            <div
              class="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center mr-4"
            >
              <span class="text-white font-bold text-xl">1</span>
            </div>
            <div>
              <h2 class="text-2xl md:text-3xl font-bold text-red-900 dark:text-red-200">
                Objective 1: Provide Contextual Information
              </h2>
              <p class="text-lg text-red-700 dark:text-red-300">
                The Foundation of Effective AI Collaboration
              </p>
            </div>
          </div>

          <div
            class="bg-white dark:bg-gray-800 rounded-lg p-6 border border-red-200 dark:border-red-800"
          >
            <h3 class="text-xl font-bold mb-4">Why Context Matters</h3>
            <div class="grid md:grid-cols-2 gap-6 text-sm">
              <div>
                <h4 class="font-semibold mb-2">🎯 Without Context:</h4>
                <ul class="space-y-1 text-gray-700 dark:text-gray-300 list-disc list-inside">
                  <li>Generic, irrelevant responses</li>
                  <li>AI doesn't understand academic level</li>
                  <li>Missing assignment-specific guidance</li>
                  <li>Wasted time with unhelpful suggestions</li>
                </ul>
              </div>
              <div>
                <h4 class="font-semibold mb-2">✅ With Proper Context:</h4>
                <ul class="space-y-1 text-gray-700 dark:text-gray-300 list-disc list-inside">
                  <li>Targeted, relevant feedback</li>
                  <li>Understanding of course level</li>
                  <li>Assignment-specific guidance</li>
                  <li>Meaningful and actionable suggestions</li>
                </ul>
              </div>
            </div>

            <div
              class="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-sm"
            >
              <p class="text-blue-900 dark:text-blue-200">
                <strong>💡 Key Point:</strong> More context (course info, goals, details) = better AI help and feedback.
              </p>
            </div>
          </div>
        </section>

        <!-- Course & Student Background -->
        <section
          class="bg-white dark:bg-gray-800 rounded-lg p-4 md:p-6 shadow-md"
        >
          <h2
            class="text-xl md:text-2xl font-bold mb-4 text-indigo-600 flex items-center gap-2"
          >
            🎓 Course & Student Background
          </h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div
              class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500"
            >
              <h3 class="font-bold text-blue-900 dark:text-blue-200 mb-3">
                Course Information
              </h3>
              <div class="space-y-1 text-sm">
                <p><strong>Course:</strong> LANG 0036 – English for Academic Purposes</p>
                <p><strong>Level:</strong> Intermediate–Advanced</p>
                <p><strong>Focus:</strong> Academic writing & critical thinking</p>
                <p><strong>Assessment:</strong> Essay writing using rubric</p>
              </div>
            </div>

            <div
              class="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500"
            >
              <h3 class="font-bold text-green-900 dark:text-green-200 mb-3">
                Student Context
              </h3>
              <div class="space-y-1 text-sm">
                <p><strong>Academic Level:</strong> University student</p>
                <p><strong>Language:</strong> English as 2nd language</p>
                <p><strong>Goals:</strong> Improve academic writing</p>
                <p><strong>Challenges:</strong> Structure, vocabulary, analysis</p>
              </div>
            </div>
          </div>

          <div
            class="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-300 dark:border-yellow-700 text-sm"
          >
            <p class="text-yellow-900 dark:text-yellow-200">
              <strong>📝 Note:</strong> Share this context when starting AI essay training for relevant feedback.
            </p>
          </div>
        </section>

        <!-- Reference Materials -->
        <section
          class="bg-white dark:bg-gray-800 rounded-lg p-4 md:p-6 shadow-md"
        >
          <h2
            class="text-xl md:text-2xl font-bold mb-4 text-indigo-600"
          >
            Reference Materials
          </h2>

          <div class="mb-6">
            <h3 class="text-lg md:text-xl font-bold mb-4 flex items-center gap-2">
              📊 Essay Assessment Rubric
            </h3>
            <div
              class="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-sm"
            >
              <p>
                <strong>📋 Contextual Information:</strong> This rubric helps AI align feedback with your course’s criteria.
              </p>
            </div>

            <div class="grid md:grid-cols-2 gap-4 text-sm">
              <div
                class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500"
              >
                <h4 class="font-bold mb-1">Content and Ideas (1–5)</h4>
                <p>Clear viewpoint, relevant ideas, addresses the question</p>
              </div>
              <div
                class="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500"
              >
                <h4 class="font-bold mb-1">Organisation & Logic (1–5)</h4>
                <p>Well‑structured, logical flow, cohesive paragraphs</p>
              </div>
              <div
                class="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border-l-4 border-purple-500"
              >
                <h4 class="font-bold mb-1">Vocabulary (1–5)</h4>
                <p>Varied and precise word choice, appropriate style</p>
              </div>
              <div
                class="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-l-4 border-orange-500"
              >
                <h4 class="font-bold mb-1">Grammar & Structure (1–5)</h4>
                <p>Accurate grammar, varied sentence structures</p>
              </div>
            </div>

            <div
              class="mt-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-300 dark:border-purple-700 text-sm"
            >
              <p class="mb-3">
                <strong>📋 Ready for copy?</strong> Get the markdown rubric below.
              </p>
              <button
                @click="openModal"
                class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg"
              >
                📋 Get Rubric Markdown
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Markdown Modal -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-2xl max-w-3xl w-full border-2 border-indigo-600 flex flex-col"
      >
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Copy Rubric Markdown</h3>
          <button
            @click="closeModal"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-300 text-2xl"
          >
            &times;
          </button>
        </div>
        <textarea
          readonly
          class="w-full h-80 p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-sm font-mono resize-none"
          v-model="rubricMarkdown"
        ></textarea>
        <div class="mt-4 flex gap-2">
          <button
            @click="copyMarkdown"
            class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg"
          >
            📋 Copy
          </button>
          <button
            @click="closeModal"
            class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const isModalOpen = ref(false);
const rubricMarkdown = `# Essay Assessment Rubric

## Content and Ideas (1–5)
Clear viewpoint, relevant ideas, addresses the question directly

## Organisation & Logic (1–5)
Well‑structured, clear paragraphs, logical flow

## Vocabulary (1–5)
Varied and precise word choice, appropriate register

## Grammar & Structure (1–5)
Accurate grammar, varied sentence structures

---
*Use this rubric to assess essay quality (1–5 scale, 5 = excellent).*`;

onMounted(() => {
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.classList.add("dark");
  }
});

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const copyMarkdown = async () => {
  await navigator.clipboard.writeText(rubricMarkdown);
  alert("Rubric markdown copied to clipboard!");
};
</script>