<template>
  <div class="avatar-panel-container">
    <!-- Avatar Panel Toggle Button -->
    <button 
      @click="togglePanel"
      class="avatar-toggle-btn"
      :class="{ 'panel-open': isVisible }"
      aria-label="Toggle Avatar Panel"
    >
      <span class="toggle-icon">{{ isVisible ? '🎭' : '💬' }}</span>
    </button>

    <!-- Avatar Panel -->
    <div 
      class="avatar-panel"
      :class="{ 'panel-visible': isVisible }"
    >
      <!-- Panel Header -->
      <div class="panel-header">
        <h3 class="panel-title">AI Tutor</h3>
        <button 
          @click="closePanel"
          class="close-btn"
          aria-label="Close Avatar Panel"
        >
          ×
        </button>
      </div>

      <!-- Avatar Placeholder (will contain AnimatedAvatar in Sprint 2) -->
      <div class="avatar-container">
        <div class="avatar-placeholder">
          <div class="placeholder-icon">🤖</div>
          <p class="placeholder-text">Avatar Coming Soon</p>
        </div>
      </div>

      <!-- Panel Footer -->
      <div class="panel-footer">
        <p class="status-text">Ready to help you learn</p>
      </div>
    </div>

    <!-- Panel Overlay (for mobile) -->
    <div 
      v-if="isVisible && isMobile"
      class="panel-overlay"
      @click="closePanel"
    ></div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'AvatarPanel',
  setup() {
    const isVisible = ref(false)
    const windowWidth = ref(window.innerWidth)

    // Computed properties
    const isMobile = computed(() => windowWidth.value < 768)

    // Methods
    const togglePanel = () => {
      isVisible.value = !isVisible.value
      // Save preference to localStorage
      localStorage.setItem('avatarPanelVisible', isVisible.value.toString())
    }

    const closePanel = () => {
      isVisible.value = false
      localStorage.setItem('avatarPanelVisible', 'false')
    }

    const handleResize = () => {
      windowWidth.value = window.innerWidth
      // Auto-close on mobile if switching to desktop
      if (!isMobile.value && isVisible.value) {
        // Keep open on desktop
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      // Restore panel state from localStorage
      const savedState = localStorage.getItem('avatarPanelVisible')
      if (savedState === 'true') {
        isVisible.value = true
      }

      // Add resize listener
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
    })

    return {
      isVisible,
      isMobile,
      togglePanel,
      closePanel
    }
  }
}
</script>

<style scoped>
.avatar-panel-container {
  position: relative;
}

/* Toggle Button */
.avatar-toggle-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-toggle-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.avatar-toggle-btn.panel-open {
  background: #f56565;
  transform: rotate(180deg);
}

.toggle-icon {
  display: block;
  transition: transform 0.3s ease;
}

/* Avatar Panel */
.avatar-panel {
  position: fixed;
  top: 0;
  right: -320px;
  width: 320px;
  height: 100vh;
  background: white;
  box-shadow: -5px 0 20px rgba(0, 0, 0, 0.1);
  z-index: 999;
  transition: right 0.3s ease;
  display: flex;
  flex-direction: column;
}

.avatar-panel.panel-visible {
  right: 0;
}

/* Panel Header */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 20px 16px;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Avatar Container */
.avatar-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.avatar-placeholder {
  text-align: center;
  color: #64748b;
}

.placeholder-icon {
  font-size: 80px;
  margin-bottom: 16px;
  opacity: 0.7;
}

.placeholder-text {
  font-size: 1rem;
  margin: 0;
  font-weight: 500;
}

/* Panel Footer */
.panel-footer {
  padding: 16px 20px 24px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  text-align: center;
}

.status-text {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
  font-style: italic;
}

/* Mobile Styles */
@media (max-width: 767px) {
  .avatar-panel {
    width: 100%;
    right: -100%;
  }
  
  .avatar-panel.panel-visible {
    right: 0;
  }

  .panel-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 998;
  }

  .avatar-toggle-btn {
    top: 16px;
    right: 16px;
    width: 48px;
    height: 48px;
    font-size: 20px;
  }
}

/* Accessibility - Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .avatar-panel,
  .avatar-toggle-btn,
  .toggle-icon {
    transition: none;
  }
}
</style>
