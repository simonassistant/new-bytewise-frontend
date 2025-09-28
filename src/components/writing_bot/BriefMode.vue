<template>
  <div class="space-y-8">
    <!-- Header Section -->
    <div class="text-center mb-8">
      <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 bg-clip-text text-transparent">
        LANG 0036: AI Writing Collaboration Lab
      </h1>
      <p class="text-xl bg-gradient-to-r from-gray-600 via-blue-500 to-purple-500 bg-clip-text text-transparent">
        Develop and demonstrate AI literacy and human-AI partnership through guided essay revision and assessment
      </p>
    </div>

    <!-- Briefing Content iFrame -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <iframe 
        src="/src/components/writing_bot/briefing.html" 
        class="w-full h-screen border-0"
        style="min-height: 800px;"
        title="Detailed Briefing Information"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
// No state management needed for iframe-only content
</script>