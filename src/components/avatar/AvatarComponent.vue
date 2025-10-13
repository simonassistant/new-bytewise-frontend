<template>
  <div
    class="relative w-48 h-48 rounded-full mx-auto overflow-hidden transition-all duration-300"
    :class="faceClasses"
  >
    <!-- Owl avatar -->
    <template v-if="state === 'speaking'">
      <video autoplay loop muted playsinline class="w-full h-full object-cover">
        <source src="./owl_animation.mp4" type="video/mp4" />
      </video>
    </template>
    <template v-else>
      <img src="./owl.png" alt="Owl Avatar" class="w-full h-full object-cover" />
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  state: {
    type: String,
    default: "idle", // idle | listening | speaking | thinking
  },
  gradientFrom: {
    type: String,
    default: "from-indigo-500",
  },
  gradientTo: {
    type: String,
    default: "to-purple-600",
  },
});

const faceClasses = computed(() => {
  return [
    "bg-gradient-to-br",
    props.gradientFrom,
    props.gradientTo,
    props.state === "listening" ? "animate-pulse shadow-xl shadow-indigo-400/50" : "",
    props.state === "speaking" ? "animate-glow" : "",
  ];
});
</script>

<style scoped>
@keyframes glow {
  0% {
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
  }
  100% {
    box-shadow: 0 0 40px rgba(102, 126, 234, 0.8);
  }
}

.animate-glow {
  animation: glow 1s infinite alternate;
}
</style>
