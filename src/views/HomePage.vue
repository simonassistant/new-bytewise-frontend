<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    <header class="bg-white/10 backdrop-blur-sm border-b border-white/20">
      <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-bold text-white">🎓 Learning Apps</h1>
        <div class="relative" ref="dropdownContainer">
          <button
            @click="showDropdown = !showDropdown"
            class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white transition"
          >
            <span>🔍</span>
            <span class="hidden sm:inline">Quick Search</span>
            <span class="text-xs opacity-70">⌘K</span>
          </button>
          
          <div
            v-if="showDropdown"
            class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl overflow-hidden z-50"
          >
            <div class="p-3 border-b">
              <input
                ref="searchInput"
                v-model="searchQuery"
                type="text"
                placeholder="Search apps..."
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                @keydown.enter="selectFirstResult"
                @keydown.escape="showDropdown = false"
              />
            </div>
            <div class="max-h-64 overflow-y-auto">
              <button
                v-for="app in filteredApps"
                :key="app.id"
                @click="selectApp(app)"
                class="w-full px-4 py-3 text-left hover:bg-indigo-50 flex items-center gap-3 transition"
              >
                <span class="text-2xl">{{ getAppIcon(app) }}</span>
                <div class="min-w-0 flex-1">
                  <div class="font-medium text-gray-800 truncate">{{ app.name }}</div>
                  <div class="text-xs text-gray-500 truncate">{{ app.welcomePrompt?.substring(0, 50) }}...</div>
                </div>
              </button>
              <div v-if="filteredApps.length === 0" class="px-4 py-6 text-center text-gray-500">
                No apps found
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-white mb-2">Welcome to the Learning Marketplace</h2>
        <p class="text-white/80">Choose an AI learning assistant to get started</p>
      </div>

      <div class="mb-6">
        <div class="flex flex-wrap gap-2 justify-center">
          <button
            v-for="cat in categories"
            :key="cat"
            @click="selectedCategory = cat"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium transition',
              selectedCategory === cat 
                ? 'bg-white text-indigo-600 shadow' 
                : 'bg-white/20 text-white hover:bg-white/30'
            ]"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="app in displayedApps"
          :key="app.id"
          class="bg-white/90 backdrop-blur rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition cursor-pointer group"
          @click="selectApp(app)"
        >
          <div :class="['h-2', app.styleClass || 'bg-gradient-to-r from-indigo-500 to-purple-600']"></div>
          <div class="p-5">
            <div class="flex items-start gap-3 mb-3">
              <span class="text-3xl">{{ getAppIcon(app) }}</span>
              <div class="min-w-0 flex-1">
                <h3 class="font-bold text-gray-800 group-hover:text-indigo-600 transition">{{ app.name }}</h3>
                <div class="flex items-center gap-2 text-xs text-gray-500 mt-1">
                  <span v-if="app.gender" class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded">
                    {{ app.gender === 'female' ? '👩' : '👨' }} Avatar
                  </span>
                </div>
              </div>
            </div>
            <p class="text-sm text-gray-600 line-clamp-2">
              {{ app.welcomePrompt || 'Start a conversation with this AI assistant.' }}
            </p>
            <button class="mt-4 w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition">
              Start Chat →
            </button>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-8">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-white/20 text-white rounded-lg disabled:opacity-40"
        >
          ← Prev
        </button>
        <span class="text-white">{{ currentPage }} / {{ totalPages }}</span>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 bg-white/20 text-white rounded-lg disabled:opacity-40"
        >
          Next →
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useChatbotStore } from '@/components/text_chatbot/chatbotStore';

const router = useRouter();
const chatbotStore = useChatbotStore();

const showDropdown = ref(false);
const searchQuery = ref("");
const selectedCategory = ref("All");
const currentPage = ref(1);
const itemsPerPage = 9;
const searchInput = ref(null);
const dropdownContainer = ref(null);

const categories = ["All", "Career", "GCAP", "IELTS", "TCM", "Other"];

onMounted(() => {
  chatbotStore.loadBots();
  document.addEventListener('keydown', handleKeydown);
  document.addEventListener('click', handleClickOutside);
});

function handleKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    showDropdown.value = !showDropdown.value;
    if (showDropdown.value) {
      nextTick(() => searchInput.value?.focus());
    }
  }
  if (e.key === 'Escape') {
    showDropdown.value = false;
  }
}

function handleClickOutside(e) {
  if (dropdownContainer.value && !dropdownContainer.value.contains(e.target)) {
    showDropdown.value = false;
  }
}

watch(showDropdown, (val) => {
  if (val) {
    nextTick(() => searchInput.value?.focus());
  }
});

const filteredApps = computed(() => {
  if (!searchQuery.value.trim()) return chatbotStore.availableBots.slice(0, 10);
  const q = searchQuery.value.toLowerCase();
  return chatbotStore.availableBots.filter(app => 
    app.name?.toLowerCase().includes(q) || 
    app.welcomePrompt?.toLowerCase().includes(q)
  );
});

const categoryFilteredApps = computed(() => {
  if (selectedCategory.value === "All") return chatbotStore.availableBots;
  
  const catMap = {
    "Career": ["cv", "cover_letter", "interview", "job", "linkedin", "networking", "aptitude"],
    "GCAP": ["gcap"],
    "IELTS": ["ielts"],
    "TCM": ["tcm"],
  };
  
  const keywords = catMap[selectedCategory.value] || [];
  if (keywords.length === 0) {
    return chatbotStore.availableBots.filter(app => {
      const id = app.id?.toLowerCase() || "";
      return !Object.values(catMap).flat().some(kw => id.includes(kw));
    });
  }
  
  return chatbotStore.availableBots.filter(app => {
    const id = app.id?.toLowerCase() || "";
    return keywords.some(kw => id.includes(kw));
  });
});

const totalPages = computed(() => Math.ceil(categoryFilteredApps.value.length / itemsPerPage));

const displayedApps = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return categoryFilteredApps.value.slice(start, start + itemsPerPage);
});

function getAppIcon(app) {
  const id = app.id?.toLowerCase() || "";
  if (id.includes("interview")) return "🎤";
  if (id.includes("cv") || id.includes("cover")) return "📄";
  if (id.includes("ielts")) return "✍️";
  if (id.includes("tcm")) return "🏥";
  if (id.includes("gcap")) return "📚";
  if (id.includes("linkedin")) return "💼";
  return "🤖";
}

function selectApp(app) {
  showDropdown.value = false;
  searchQuery.value = "";
  router.push({ name: 'Chat', params: { appId: app.id } });
}

function selectFirstResult() {
  if (filteredApps.value.length > 0) {
    selectApp(filteredApps.value[0]);
  }
}

watch(selectedCategory, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
