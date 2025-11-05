<template>
  <div class="chat-interface flex-1 flex flex-col">
    <div class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
      <div class="w-full mx-auto flex flex-1 gap-4">
        <!-- Left: Chat messages + input -->
        <div class="flex flex-col w-1/2" style="height: 70vh">
          <!-- Chat history -->
          <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
            <div
              v-for="(msg, i) in activeChatHistory"
              :key="i"
              class="flex"
              :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-lg md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
                :class="msgClasses(msg)"
              >
                <div class="font-semibold text-xs mb-1">
                  {{ msgSenderLabel(msg.role) }}
                </div>
                <div
                  class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
                  v-html="renderMarkdown(msg.content)"
                />
                <div class="text-xs text-gray-400 mt-2 text-right">
                  {{ msg.timestamp.toLocaleTimeString() }}
                </div>
              </div>
            </div>
          </div>

          <!-- Chat input -->
          <div class="mt-3 flex gap-2 items-start relative">
            <div class="flex-1 flex flex-col-reverse">
              <!-- Textarea -->
              <textarea
                v-model="localUserMessage"
                :style="{ height: inputHeight + 'px' }"
                :placeholder="
                  isConnected ? 'Type your message...' : 'Please connect to API first...'
                "
                class="border rounded-lg p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed w-full"
                @keyup.enter.exact.prevent="$emit('sendMessage')"
                :disabled="isThinking || !isConnected"
                ref="chatInput"
              ></textarea>

              <!-- Drag handle above input -->
              <div
                class="h-2 cursor-ns-resize bg-transparent hover:bg-indigo-200 transition-colors rounded-t-lg"
                @mousedown="startDrag"
                @touchstart.prevent="startDrag"
              ></div>
            </div>

            <button
              @click="$emit('sendMessage')"
              class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed h-fit"
              :disabled="isThinking || !isConnected || isSubmitted"
            >
              {{ isThinking ? "Thinking..." : "Send" }}
            </button>
          </div>
        </div>

        <!-- Right: Draft area -->
        <div class="flex-1 space-y-4 overflow-y-auto h-full">
          <!-- Original Draft -->
          <div class="bg-white p-4 rounded-lg shadow">
            <h2 class="text-lg font-bold mb-2">
              {{ currentMode === "assessment" ? "Your Original Essay" : "Original Draft" }}
            </h2>
            <textarea
              v-model="localOriginalDraft"
              rows="9"
              :placeholder="
                currentMode === 'assessment'
                  ? 'Paste your original essay here...'
                  : 'Paste or write the original draft here...'
              "
              class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              :disabled="
                (isOriginalDraftConfirmed && currentMode === 'assessment') ||
                currentMode === 'training'
              "
            />
            <button
              @click="$emit('confirmDraft')"
              class="w-full mt-2 px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="currentMode !== 'assessment' || isOriginalDraftConfirmed"
            >
              {{
                currentMode === "assessment"
                  ? isOriginalDraftConfirmed
                    ? "Essay Confirmed"
                    : "Confirm Your Essay"
                  : "Modification is not allowed in Training Mode"
              }}
            </button>
          </div>

          <!-- Final Draft -->
          <div class="bg-white p-4 rounded-lg shadow">
            <h2 class="text-lg font-bold mb-2">
              {{ currentMode === "assessment" ? "Revised Version (Auto-Updated)" : "Final Draft" }}
            </h2>
            <div class="relative w-full">
              <div v-if="isUpdatingDraft" class="p-3 text-gray-500 text-sm italic">
                Updating draft...
              </div>

              <textarea
                v-else
                v-model="localFinalDraft"
                rows="9"
                :placeholder="
                  currentMode === 'assessment'
                    ? 'This will be updated automatically as you revise through chat...'
                    : 'Paste or write the improved draft here...'
                "
                class="w-full border rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                :disabled="currentMode === 'assessment' && isOriginalDraftConfirmed"
                :readonly="currentMode === 'assessment'"
              />
            </div>
            <button
              @click="
                currentMode === 'assessment'
                  ? $emit('submitAssessment')
                  : $emit('confirmFinalDraft')
              "
              class="w-full mt-2 px-3 py-2 text-white rounded-lg text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
              :class="currentMode === 'assessment' ? 'bg-green-600' : 'bg-blue-600'"
              :disabled="
                (!isOriginalDraftConfirmed && currentMode === 'assessment') ||
                isGeneratingAssessment ||
                isSubmitted
              "
            >
              <span v-if="isGeneratingAssessment">
                {{
                  currentMode === "assessment"
                    ? "🔄 Generating Assessment..."
                    : "🔄 Generating Report..."
                }}
              </span>
              <span v-else>
                {{
                  currentMode === "assessment"
                    ? "Submit Assessment"
                    : "Confirm Final Draft & Generate Report"
                }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import MarkdownIt from "markdown-it";

// ========= Props & Emits ========= //
const props = defineProps({
  activeChatHistory: Array,
  currentMode: String,
  isConnected: Boolean,
  isThinking: Boolean,
  isUpdatingDraft: Boolean,
  isSubmitted: Boolean,
  isGeneratingAssessment: Boolean,
  isOriginalDraftConfirmed: Boolean,
  userMessage: String,
  originalDraft: String,
  finalDraft: String,
});

const emits = defineEmits([
  "update:userMessage",
  "update:originalDraft",
  "update:finalDraft",
  "sendMessage",
  "confirmDraft",
  "submitAssessment",
  "confirmFinalDraft",
]);

// ========= Reactive State ========= //
const localUserMessage = ref(props.userMessage);
const localOriginalDraft = ref(props.originalDraft);
const localFinalDraft = ref(props.finalDraft);

// Utility: sync two-way model automatically
const bindSync = (localRef, propName) => {
  watch(localRef, (v) => emits(`update:${propName}`, v));
  watch(
    () => props[propName],
    (v) => (localRef.value = v)
  );
};

bindSync(localUserMessage, "userMessage");
bindSync(localOriginalDraft, "originalDraft");
bindSync(localFinalDraft, "finalDraft");

// ========= Markdown Renderer ========= //
const markdown = new MarkdownIt({ linkify: true, typographer: true });
const renderMarkdown = (text = "") => markdown.render(text);

// ========= Message Display Helpers ========= //
const msgSenderLabel = (role) => (role === "user" ? "You" : "AI Assistant");
const msgClasses = (msg) =>
  msg.role === "user"
    ? "bg-indigo-600 text-white rounded-br-none"
    : "bg-gray-100 text-gray-800 rounded-bl-none";

// ========= Auto-scroll to latest message ========= //
const chatMessages = ref(null);
function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
  });
}
watch(() => props.activeChatHistory?.length, scrollToBottom, { flush: "post" });

// ========= Resizable Chat Input ========= //
const chatInput = ref(null);
const inputHeight = ref(80);
let dragState = { startY: 0, startHeight: 0 };

function startDrag(e) {
  const y = e.touches?.[0]?.clientY ?? e.clientY;
  dragState = { startY: y, startHeight: chatInput.value.offsetHeight };

  const move = (ev) => {
    const currentY = ev.touches?.[0]?.clientY ?? ev.clientY;
    const diff = dragState.startY - currentY;
    inputHeight.value = Math.max(60, Math.min(400, dragState.startHeight + diff));
  };
  const stop = () => {
    window.removeEventListener("mousemove", move);
    window.removeEventListener("mouseup", stop);
    window.removeEventListener("touchmove", move);
    window.removeEventListener("touchend", stop);
  };

  window.addEventListener("mousemove", move);
  window.addEventListener("mouseup", stop);
  window.addEventListener("touchmove", move);
  window.addEventListener("touchend", stop);
}
</script>
