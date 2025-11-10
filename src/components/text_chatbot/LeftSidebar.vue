<template>
  <aside
    class="bg-white/90 backdrop-blur shadow-xl flex flex-col transition-all duration-300 overflow-hidden"
    :class="isOpen ? 'w-80' : 'w-0'"
  >
    <!-- Header -->
    <div
      v-if="isOpen"
      class="p-5 border-b bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex justify-between items-center"
    >
      <h2 class="text-lg font-bold flex items-center gap-2">🤖 Chatbot Configuration</h2>
      <button class="text-white hover:text-gray-200" @click="$emit('update:isOpen', false)">
        ✖
      </button>
    </div>

    <!-- Content -->
    <div v-if="isOpen" class="p-5 space-y-6 flex-1 overflow-y-auto">
      <!-- API Config -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <h3 class="font-semibold text-yellow-800 mb-3">🔑 API Configuration</h3>
        <input
          type="password"
          :value="apiKey"
          @input="onApiKeyInput($event.target.value)"
          placeholder="Paste your API key..."
          class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
        />
        <p class="text-xs text-gray-600 mt-2" v-if="selectedProvider === 'hkbu'">
          Get your key from the
          <a
            href="https://genai.hkbu.edu.hk/settings/api-docs"
            target="_blank"
            rel="noopener noreferrer"
            class="text-indigo-600 hover:underline"
          >
            HKBU Generative AI Platform </a
          >.
        </p>
        <p class="text-xs text-green-700 mt-2" v-if="selectedProvider === 'openrouter'">
          ✅ Using <strong>OpenRouter</strong> as provider (via <code>feelinglucky</code>).
        </p>
      </div>

      <!-- Model Selector -->
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 class="font-semibold mb-3">🤖 Choose Model</h3>
        <select
          :value="model"
          @change="$emit('update:model', $event.target.value)"
          class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
        >
          <option value="gpt-5-mini" v-if="selectedProvider === 'hkbu'">GPT-5 Mini</option>
          <option value="gpt-5" v-if="selectedProvider === 'hkbu'">GPT-5</option>
          <option value="gpt-4.1-mini">GPT-4.1 Mini</option>
          <option value="gpt-4.1">GPT-4.1</option>
          <option value="gpt-4o" v-if="selectedProvider === 'openrouter'">GPT-4o</option>
        </select>
      </div>

      <!-- Buttons -->
      <div class="flex gap-2 mt-3">
        <button
          class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium"
          @click="$emit('connectAPI')"
          :disabled="isConnecting || isConnected"
        >
          <span v-if="isConnecting">🔄 Connecting...</span>
          <span v-else-if="isConnected">✔️ Connected</span>
          <span v-else>✅ Connect</span>
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 text-gray-700 text-sm font-medium"
          @click="$emit('clearAPI')"
          :disabled="isConnecting"
        >
          🗑️ Clear
        </button>
      </div>

      <!-- Prompts -->
      <div>
        <h3 class="font-semibold mb-2">⚙️ System Prompt</h3>
        <div class="bg-gray-100 p-3 rounded-lg text-sm shadow-inner whitespace-pre-line">
          {{ systemPrompt }}
        </div>
      </div>

      <!-- Token Usage -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 class="font-semibold text-blue-800 mb-2">📊 Token Usage</h3>
        <p class="text-sm text-blue-900">
          Estimated tokens used:
          <span class="font-bold">{{ tokenUsage }}</span>
        </p>
      </div>
    </div>
  </aside>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
const props = defineProps({
  isOpen: Boolean,
  systemPrompt: String,
  welcomePrompt: String,
  model: String,
  apiKey: String,
  isConnected: Boolean,
  tokenUsage: Number,
  selectedProvider: String,
  isConnecting: Boolean,
});

const emit = defineEmits([
  "update:isOpen",
  "update:apiKey",
  "update:model",
  "update:selectedProvider",
  "connectAPI",
  "clearAPI",
]);

function onApiKeyInput(value) {
  emit("update:apiKey", value);
  if (value.trim() === "feelinglucky") {
    emit("update:selectedProvider", "openrouter");
  } else {
    emit("update:selectedProvider", "hkbu");
  }
}
</script>
