<template>
  <div class="p-4 bg-gray-50 rounded-lg mb-6">
    <h2 class="text-xl font-bold text-gray-900 mb-4 text-center">📝 Course & Student Background</h2>

    <!-- Course Information -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">📘 Course Information</h3>
    <div class="overflow-x-auto mb-6">
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

    <!-- Student Context -->
    <h3 class="text-lg font-semibold mb-2 text-gray-800">🎓 Student Context</h3>
    <div class="overflow-x-auto mb-6">
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

    <!-- Rubrics Input -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 mb-6">
      <h3 class="font-semibold text-gray-900 mb-2">📊 Rubrics Input</h3>
      <textarea
        v-model="localRubric"
        placeholder="Paste or type your rubric here..."
        rows="6"
        class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring focus:ring-indigo-300"
      ></textarea>
    </div>

    <!-- Buttons -->
    <div class="flex justify-center gap-4">
      <button
        @click="handleSubmit"
        class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-6 py-2 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 transition"
      >
        Submit
      </button>

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
import { reactive, watch, ref } from "vue";

const props = defineProps({
  courseInfo: {
    type: Object,
    required: true,
  },
  studentContext: {
    type: Object,
    required: true,
  },
  rubric: {
    type: String,
    default: "",
  },
});
const emit = defineEmits(["submit", "update:courseInfo", "update:studentContext"]);

const localRubric = ref(props.rubric || "");
const localCourseInfo = reactive({ ...props.courseInfo });
const localStudentContext = reactive({ ...props.studentContext });

watch(localCourseInfo, (val) => emit("update:courseInfo", { ...val }), { deep: true });
watch(localStudentContext, (val) => emit("update:studentContext", { ...val }), { deep: true });

/** Format display label */
function formatLabel(key) {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}
function hasEmptyFields(obj) {
  return Object.values(obj).some((val) => !val || !val.trim());
}

/** Submit the data */
function handleSubmit() {
  if (hasEmptyFields(localCourseInfo)||hasEmptyFields(localStudentContext)) {
    alert("Please fill in all Course Information and Student Context fields before submitting.");
    return;
  }
  if (!localRubric.value.trim()) {
    alert("Please provide the rubric before submitting.");
    return;
  }
  emit("submit", {
    courseInfo: { ...localCourseInfo },
    studentContext: { ...localStudentContext },
    rubric: localRubric.value,
  });
}

/** Clear all input fields */
function handleClearAll() {
  for (const key in localCourseInfo) localCourseInfo[key] = "";
  for (const key in localStudentContext) localStudentContext[key] = "";
  localRubric.value = "";
}
</script>
