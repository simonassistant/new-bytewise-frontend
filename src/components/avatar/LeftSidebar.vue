<template>
  <aside
    class="bg-white/90 backdrop-blur shadow-xl flex flex-col transition-all duration-300 overflow-hidden"
    :class="[
      isOpen ? 'w-80' : 'w-0',
      'md:relative fixed left-0 top-0 h-full z-50 md:z-auto'
    ]"
  >
    <!-- Header -->
    <div
      v-if="isOpen"
      class="p-4 sm:p-5 border-b bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex justify-between items-center"
    >
      <h2 class="text-base sm:text-lg font-bold flex items-center gap-2">📧 Email Configuration</h2>
      <button class="text-white hover:text-gray-200 text-xl sm:text-2xl" @click="$emit('update:isOpen', false)">
        ✖
      </button>
    </div>

    <!-- Content -->
    <div v-if="isOpen" class="p-4 sm:p-5 space-y-4 sm:space-y-6 flex-1 overflow-y-auto">
      <!-- User Information -->
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 sm:p-4 space-y-3 sm:space-y-4">
        <h3 class="font-semibold text-sm sm:text-base text-gray-800 mb-2 sm:mb-3">👤 User Information</h3>

        <!-- Name Input -->
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Full Name</label>
          <input
            type="text"
            v-model="name"
            @input="emitUserData"
            placeholder="Enter your name"
            class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
          />
        </div>

        <!-- Email Input (Two Rows) -->
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Email</label>

          <!-- Row 1: Local part -->
          <input
            type="text"
            v-model="emailLocal"
            @input="emitUserData"
            placeholder="Enter student/staff email"
            class="w-full border rounded-lg p-2 text-sm mb-2 focus:ring focus:ring-indigo-300"
          />

          <!-- Row 2: Domain selector -->
          <select
            v-model="emailSuffix"
            @change="emitUserData"
            class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
          >
            <option value="@hkbu.edu.hk">@hkbu.edu.hk</option>
            <option value="@life.hkbu.edu.hk">@life.hkbu.edu.hk</option>
          </select>
        </div>
      </div>

      <!-- Token Usage -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 sm:p-4">
        <h3 class="font-semibold text-sm sm:text-base text-blue-800 mb-2">📊 Token Usage</h3>
        <p class="text-xs sm:text-sm text-blue-900">
          Estimated tokens used:
          <span class="font-bold">{{ tokenUsage }}</span>
        </p>
      </div>
    </div>

  </aside>
</template>

<script setup>
import { ref, watch } from "vue";

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  isOpen: Boolean,
  tokenUsage: Number,
});

const emit = defineEmits(["update:isOpen", "updateUserData"]);

const name = ref("");
const emailLocal = ref("");
const emailSuffix = ref("@hkbu.edu.hk");

// Emit combined data
function emitUserData() {
  const fullEmail = emailLocal.value ? `${emailLocal.value}${emailSuffix.value}` : "";
  emit("updateUserData", {
    name: name.value,
    email: fullEmail,
  });
}

// Automatically emit updates when values change
watch([name, emailLocal, emailSuffix], emitUserData);
</script>

<style scoped>
aside {
  transition: width 0.3s ease;
}
</style>