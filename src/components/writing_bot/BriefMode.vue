<template>
  <div class="space-y-8">
    <!-- Briefing Content iFrame -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <iframe
        src="/briefing.html"
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