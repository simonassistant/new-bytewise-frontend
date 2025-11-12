<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="close"
  >
    <div
      class="bg-white rounded-lg shadow-xl w-full max-w-md p-6 text-center relative animate-fadeIn"
    >
      <!-- Header -->
      <h2 class="text-xl font-bold text-gray-800 mb-2">Assessment Submitted 🎉</h2>
      <p class="text-gray-600 mb-4">
        Your assessment has been submitted successfully!<br />
        Please rate your experience below 👇
      </p>

      <!-- Star Rating -->
      <div class="flex justify-center mb-3">
        <span
          v-for="n in 5"
          :key="n"
          class="text-3xl cursor-pointer transition-colors"
          :class="n <= rating ? 'text-yellow-400' : 'text-gray-300'"
          @click="rating = n"
        >
          ★
        </span>
      </div>

      <!-- Comment Box -->
      <textarea
        v-model="comment"
        placeholder="Leave a comment (optional)..."
        class="w-full border border-gray-300 rounded-md p-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
      ></textarea>

      <!-- Buttons -->
      <div class="flex justify-end gap-2">
        <button
          @click="close"
          class="px-4 py-2 rounded-lg bg-gray-300 text-gray-700 hover:bg-gray-400 transition"
        >
          Cancel
        </button>
        <button
          @click="submit"
          :disabled="loading"
          class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition disabled:bg-blue-300"
        >
          {{ loading ? "Submitting..." : "Submit" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { BASE_URL } from "@/components/base_url";

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  show: Boolean,
});

const emit = defineEmits(["close", "submit"]);

const rating = ref(0);
const comment = ref("");
const loading = ref(false);

function close() {
  rating.value = 0;
  comment.value = "";
  emit("close");
}

async function submit() {
  if (!rating.value) {
    alert("Please select a rating before submitting!");
    return;
  }

  loading.value = true;

  try {
    const response = await fetch(`${BASE_URL}/supabase/add_comment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        rating: rating.value,
        comment: comment.value,
      }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Successfully sent to backend:", data);

    emit("submit", { rating: rating.value, comment: comment.value });
    alert("Thank you for your feedback!");
    close();
  } catch (error) {
    console.error("❌ Error submitting comment:", error);
    alert("Failed to submit feedback. Please try again later.");
  } finally {
    loading.value = false;
  }
}
</script>