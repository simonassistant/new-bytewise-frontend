<template>
  <div class="input-mode-toggle-container">
    <div class="toggle-wrapper">
      <!-- Mode Labels -->
      <div class="mode-labels">
        <span 
          class="mode-label"
          :class="{ 'active': currentMode === 'typing' }"
        >
          ⌨️ Type
        </span>
        <span 
          class="mode-label"
          :class="{ 'active': currentMode === 'voice' }"
        >
          🎤 Voice
        </span>
      </div>

      <!-- Toggle Switch -->
      <div 
        class="toggle-switch"
        @click="toggleMode"
        :class="{ 'voice-mode': currentMode === 'voice' }"
        role="switch"
        :aria-checked="currentMode === 'voice'"
        tabindex="0"
        @keydown="handleKeydown"
      >
        <div class="toggle-slider">
          <div class="slider-icon">
            {{ currentMode === 'typing' ? '⌨️' : '🎤' }}
          </div>
        </div>
      </div>

      <!-- Mode Description -->
      <div class="mode-description">
        <p class="description-text">
          {{ currentMode === 'typing' 
            ? 'Type your messages in the text box' 
            : 'Click and speak your message aloud' 
          }}
        </p>
      </div>
    </div>

    <!-- Status Indicator -->
    <div v-if="showStatus" class="status-indicator">
      <div class="status-dot" :class="statusClass"></div>
      <span class="status-text">{{ statusMessage }}</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'

export default {
  name: 'InputModeToggle',
  props: {
    initialMode: {
      type: String,
      default: 'typing',
      validator: (value) => ['typing', 'voice'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    },
    showStatus: {
      type: Boolean,
      default: true
    }
  },
  emits: ['mode-changed'],
  setup(props, { emit }) {
    const currentMode = ref(props.initialMode)
    const isTransitioning = ref(false)

    // Status management
    const statusMessage = computed(() => {
      if (props.disabled) return 'Mode switching disabled'
      if (isTransitioning.value) return 'Switching mode...'
      
      switch (currentMode.value) {
        case 'typing':
          return 'Ready for text input'
        case 'voice':
          return 'Ready for voice input'
        default:
          return 'Ready'
      }
    })

    const statusClass = computed(() => {
      if (props.disabled) return 'status-disabled'
      if (isTransitioning.value) return 'status-transitioning'
      return 'status-ready'
    })

    // Methods
    const toggleMode = () => {
      if (props.disabled || isTransitioning.value) return

      isTransitioning.value = true
      
      // Add slight delay for smooth transition
      setTimeout(() => {
        const newMode = currentMode.value === 'typing' ? 'voice' : 'typing'
        currentMode.value = newMode
        
        // Save preference
        localStorage.setItem('inputMode', newMode)
        
        // Emit change event
        emit('mode-changed', newMode)
        
        // Reset transition state
        setTimeout(() => {
          isTransitioning.value = false
        }, 150)
      }, 100)
    }

    const handleKeydown = (event) => {
      if (event.key === ' ' || event.key === 'Enter') {
        event.preventDefault()
        toggleMode()
      }
    }

    const setMode = (mode) => {
      if (['typing', 'voice'].includes(mode)) {
        currentMode.value = mode
        localStorage.setItem('inputMode', mode)
        emit('mode-changed', mode)
      }
    }

    // Lifecycle
    onMounted(() => {
      // Restore mode from localStorage
      const savedMode = localStorage.getItem('inputMode')
      if (savedMode && ['typing', 'voice'].includes(savedMode)) {
        currentMode.value = savedMode
        emit('mode-changed', savedMode)
      }
    })

    // Watch for external mode changes
    watch(() => props.initialMode, (newMode) => {
      if (newMode !== currentMode.value) {
        currentMode.value = newMode
      }
    })

    return {
      currentMode,
      isTransitioning,
      statusMessage,
      statusClass,
      toggleMode,
      handleKeydown,
      setMode
    }
  }
}
</script>

<style scoped>
.input-mode-toggle-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

/* Toggle Wrapper */
.toggle-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

/* Mode Labels */
.mode-labels {
  display: flex;
  gap: 24px;
  margin-bottom: 8px;
}

.mode-label {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  transition: color 0.2s ease;
  user-select: none;
}

.mode-label.active {
  color: #2196F3;
  font-weight: 600;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  width: 80px;
  height: 40px;
  background: #e2e8f0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  outline: none;
}

.toggle-switch:hover {
  background: #cbd5e1;
  transform: scale(1.02);
}

.toggle-switch:focus {
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

.toggle-switch.voice-mode {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.toggle-switch.voice-mode:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

/* Toggle Slider */
.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 36px;
  height: 36px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.voice-mode .toggle-slider {
  transform: translateX(40px);
}

.slider-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.toggle-switch:active .slider-icon {
  transform: scale(0.9);
}

/* Mode Description */
.mode-description {
  text-align: center;
  max-width: 200px;
}

.description-text {
  margin: 0;
  font-size: 13px;
  color: #64748b;
  line-height: 1.3;
}

/* Status Indicator */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.status-ready {
  background-color: #10b981;
  animation: pulse 2s infinite;
}

.status-transitioning {
  background-color: #f59e0b;
  animation: blink 0.5s infinite;
}

.status-disabled {
  background-color: #6b7280;
}

.status-text {
  font-size: 12px;
  color: #4b5563;
  font-weight: 500;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* Mobile Responsive */
@media (max-width: 640px) {
  .input-mode-toggle-container {
    padding: 12px;
  }

  .mode-labels {
    gap: 16px;
  }

  .mode-label {
    font-size: 13px;
  }

  .toggle-switch {
    width: 70px;
    height: 36px;
  }

  .toggle-slider {
    width: 32px;
    height: 32px;
  }

  .voice-mode .toggle-slider {
    transform: translateX(34px);
  }

  .description-text {
    font-size: 12px;
  }
}

/* Disabled State */
.toggle-switch:disabled,
.toggle-switch.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .toggle-switch {
    border: 2px solid #000;
  }
  
  .mode-label {
    font-weight: 600;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .toggle-switch,
  .toggle-slider,
  .slider-icon,
  .status-dot {
    transition: none;
    animation: none;
  }
}
</style>
