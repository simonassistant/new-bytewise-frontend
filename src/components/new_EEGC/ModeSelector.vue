<template>
  <div class="mb-6 p-4 bg-gray-50 rounded-lg">
    <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
      <!-- Mode Buttons -->
      <div class="flex gap-4">
        <button
          v-for="mode in modes"
          :key="mode"
          @click="$emit('switch-mode', mode)"
          :class="[
            currentMode === mode ? activeBtn : inactiveBtn,
            isThinking ? 'cursor-not-allowed opacity-50' : '',
          ]"
          :disabled="isThinking"
        >
          {{ mode.charAt(0).toUpperCase() + mode.slice(1) }} Mode
        </button>
      </div>

      <!-- Mode Label -->
      <div class="px-4 py-2 rounded-full text-sm font-medium" :class="modeColors[currentMode]">
        {{ modeLabels[currentMode] }}
      </div>
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
const props = defineProps({
  currentMode: { type: String, required: true },
  isThinking: { type: Boolean, required: true },
  modeLabels: { type: Object, required: true },
  modeColors: { type: Object, required: true },
});

defineEmits(["switch-mode"]);

const modes = ["briefing", "training", "assessment"];

const activeBtn = "px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold";
const inactiveBtn = "px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-semibold";
</script>
