<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    <header class="bg-white/10 backdrop-blur-sm border-b border-white/20">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-bold text-white">🎓 Learning Apps</h1>
        <div class="flex gap-2 flex-wrap">
          <div v-for="cat in categories" :key="cat.key" class="relative" :ref="el => dropdownRefs[cat.key] = el">
            <button
              @click="toggleDropdown(cat.key)"
              class="flex items-center gap-1 px-3 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white text-sm transition"
            >
              <span>{{ cat.icon }}</span>
              <span class="hidden sm:inline">{{ cat.label }}</span>
              <span class="text-xs">▼</span>
            </button>
            
            <div
              v-if="openDropdown === cat.key"
              class="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-2xl overflow-hidden z-50"
            >
              <div class="p-2 border-b">
                <input
                  v-model="dropdownSearch[cat.key]"
                  type="text"
                  :placeholder="`Search ${cat.label}...`"
                  class="w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  @keydown.escape="openDropdown = null"
                />
              </div>
              <div class="max-h-64 overflow-y-auto">
                <button
                  v-for="app in getFilteredAppsForCategory(cat.key)"
                  :key="app.id"
                  @click="selectApp(app)"
                  class="w-full px-3 py-2 text-left hover:bg-indigo-50 flex items-center gap-2 transition text-sm"
                >
                  <span>{{ getAppIcon(app) }}</span>
                  <span class="truncate">{{ app.name }}</span>
                </button>
                <div v-if="getFilteredAppsForCategory(cat.key).length === 0" class="px-3 py-4 text-center text-gray-500 text-sm">
                  No apps found
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-white mb-2">Welcome to the Learning Marketplace</h2>
        <p class="text-white/80">Choose an AI learning assistant to get started</p>
      </div>

      <div v-for="cat in categories" :key="cat.key" class="mb-10">
        <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>{{ cat.icon }}</span> {{ cat.label }}
          <span class="text-sm font-normal opacity-70">({{ getAppsForCategory(cat.key).length }})</span>
        </h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div
            v-for="app in getAppsForCategory(cat.key)"
            :key="app.id"
            class="bg-white/90 backdrop-blur rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition cursor-pointer group"
            @click="selectApp(app)"
          >
            <div :class="['h-1.5', app.styleClass || 'bg-gradient-to-r from-indigo-500 to-purple-600']"></div>
            <div class="p-4">
              <div class="flex items-start gap-2 mb-2">
                <span class="text-2xl">{{ getAppIcon(app) }}</span>
                <div class="min-w-0 flex-1">
                  <h4 class="font-bold text-gray-800 group-hover:text-indigo-600 transition text-sm leading-tight">{{ app.name }}</h4>
                  <span v-if="app.gender" class="text-xs px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded">
                    {{ app.gender === 'female' ? '👩' : '👨' }}
                  </span>
                </div>
              </div>
              <p class="text-xs text-gray-600 line-clamp-2 mb-3">
                {{ app.welcomePrompt || 'Start a conversation with this AI assistant.' }}
              </p>
              <button class="w-full py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-medium transition">
                Start Chat →
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="getAppsForCategory(cat.key).length === 0" class="text-center py-8 text-white/60">
          No apps in this category yet
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useChatbotStore } from '@/components/text_chatbot/chatbotStore';

const router = useRouter();
const chatbotStore = useChatbotStore();

const openDropdown = ref(null);
const dropdownRefs = reactive({});
const dropdownSearch = reactive({
  career: '',
  gcap: '',
  ielts: '',
  tcm: '',
  other: ''
});

const categories = [
  { key: 'career', label: 'Career', icon: '💼' },
  { key: 'gcap', label: 'GCAP', icon: '📚' },
  { key: 'ielts', label: 'IELTS', icon: '✍️' },
  { key: 'tcm', label: 'TCM', icon: '🏥' },
  { key: 'other', label: 'Other', icon: '🤖' }
];

const categoryKeywords = {
  career: ['cv', 'cover_letter', 'interview', 'job', 'linkedin', 'networking', 'aptitude', 'career'],
  gcap: ['gcap'],
  ielts: ['ielts'],
  tcm: ['tcm']
};

onMounted(() => {
  chatbotStore.loadBots();
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleKeydown);
});

function handleClickOutside(e) {
  if (openDropdown.value) {
    const ref = dropdownRefs[openDropdown.value];
    if (ref && !ref.contains(e.target)) {
      openDropdown.value = null;
    }
  }
}

function handleKeydown(e) {
  if (e.key === 'Escape') {
    openDropdown.value = null;
  }
}

function toggleDropdown(key) {
  openDropdown.value = openDropdown.value === key ? null : key;
}

function getAppsForCategory(catKey) {
  const keywords = categoryKeywords[catKey];
  
  if (!keywords) {
    return chatbotStore.availableBots.filter(app => {
      const id = app.id?.toLowerCase() || '';
      return !Object.values(categoryKeywords).flat().some(kw => id.includes(kw));
    });
  }
  
  return chatbotStore.availableBots.filter(app => {
    const id = app.id?.toLowerCase() || '';
    return keywords.some(kw => id.includes(kw));
  });
}

function getFilteredAppsForCategory(catKey) {
  const apps = getAppsForCategory(catKey);
  const search = dropdownSearch[catKey]?.toLowerCase() || '';
  if (!search) return apps;
  return apps.filter(app => 
    app.name?.toLowerCase().includes(search) ||
    app.welcomePrompt?.toLowerCase().includes(search)
  );
}

function getAppIcon(app) {
  const id = app.id?.toLowerCase() || '';
  if (id.includes('interview')) return '🎤';
  if (id.includes('cv') || id.includes('cover')) return '📄';
  if (id.includes('ielts')) return '✍️';
  if (id.includes('tcm')) return '🏥';
  if (id.includes('gcap')) return '📚';
  if (id.includes('linkedin')) return '💼';
  return '🤖';
}

function selectApp(app) {
  openDropdown.value = null;
  router.push({ name: 'Chat', params: { appId: app.id } });
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
