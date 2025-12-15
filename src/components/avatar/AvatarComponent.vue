<template>
  <div
    v-if="assetsLoaded"
    class="relative w-full h-full rounded-full mx-auto overflow-hidden transition-all duration-300"
    :class="faceClasses"
  >
    <!-- Speaking animation (video) -->
    <video
      autoplay
      loop
      muted
      playsinline
      preload="auto"
      class="avatar-media w-full h-full object-cover absolute top-0 left-0 transition-opacity duration-300"
      :class="{ 'opacity-100': state === 'speaking', 'opacity-0': state !== 'speaking' }"
      ref="videoRef"
    >
      <source :src="videoSrc" type="video/mp4" />
    </video>
    <!-- Owl avatar -->
    <img
      :src="imageSrc"
      alt="Avatar"
      class="avatar-media w-full h-full object-cover absolute top-0 left-0 transition-opacity duration-300"
      :class="{ 'opacity-0': state === 'speaking', 'opacity-100': state !== 'speaking' }"
    />
  </div>

  <!-- Optional Loader / Placeholder -->
  <div
    v-else
    class="w-full h-full flex items-center justify-center text-gray-500 mx-auto text-sm sm:text-base"
  >
    Loading...
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({
  state: {
    type: String,
    default: "idle",
  },
  gender: {
    type: String,
    default: "male",
  },
  appearance: {
    type: String,
    default: "asain",
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

const assetsLoaded = ref(false);

// Dynamically set image and video based on gender
const imageSrc = computed(() => {
  const isFemale = props.gender === "female";
  const appearance = props.appearance; // or props.apperance if that's the actual prop

  if (appearance.includes("Mr")) {
    return new URL(`./${appearance}.png`, import.meta.url).href;
  }

  if (appearance === "asian") {
    return isFemale
      ? new URL("./asian_woman.jpg", import.meta.url).href
      : new URL("./asian_man.jpg", import.meta.url).href;
  } else {
    return isFemale
      ? new URL("./western_woman.jpg", import.meta.url).href
      : new URL("./western_man.jpg", import.meta.url).href;
  }
});

const videoSrc = computed(() => {
  const isFemale = props.gender === "female";
  const appearance = props.appearance; // or props.apperance
  if (appearance.includes("Mr")) {
    return new URL(`./${appearance}_talk.mp4`, import.meta.url).href;
  }
  if (appearance === "asian") {
    return isFemale
      ? new URL("./asian_woman_talk.mp4", import.meta.url).href
      : new URL("./asian_man_talk.mp4", import.meta.url).href;
  } else {
    return isFemale
      ? new URL("./western_woman_talk.mp4", import.meta.url).href
      : new URL("./western_man_talk.mp4", import.meta.url).href;
  }
});

// Preload functions
const preloadImage = (src) =>
  new Promise((resolve, reject) => {
    const img = new Image();
    img.src = src;
    img.onload = resolve;
    img.onerror = reject;
  });

const preloadVideo = (src) =>
  new Promise((resolve, reject) => {
    const video = document.createElement("video");
    video.src = src;
    video.preload = "auto";
    video.oncanplaythrough = resolve;
    video.onerror = reject;
  });

onMounted(async () => {
  try {
    await Promise.all([preloadImage(imageSrc.value), preloadVideo(videoSrc.value)]);
  } catch (err) {
    console.warn("Asset preload failed:", err);
  } finally {
    assetsLoaded.value = true;
  }
});

// Reactive face classes for animations
const faceClasses = computed(() => [
  "bg-gradient-to-br",
  props.gradientFrom,
  props.gradientTo,
  props.state === "listening" ? "animate-pulse shadow-xl shadow-indigo-400/50" : "",
  props.state === "speaking" ? "animate-glow" : "",
]);
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
