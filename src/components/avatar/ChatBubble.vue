<template>
  <div 
    class="chat-bubble-wrapper"
    :class="messageTypeClass"
  >
    <!-- Avatar -->
    <div class="message-avatar">
      <div v-if="isUser" class="user-avatar">
        {{ userInitial }}
      </div>
      <div v-else class="ai-avatar">
        🤖
      </div>
    </div>

    <!-- Message Bubble -->
    <div 
      class="message-bubble"
      :class="bubbleClass"
      @mouseenter="showTimestamp = true"
      @mouseleave="showTimestamp = false"
    >
      <!-- Message Content -->
      <div class="message-content">
        <p class="message-text" v-html="formattedMessage"></p>
      </div>

      <!-- Timestamp (shown on hover) -->
      <div 
        v-if="showTimestamp"
        class="message-timestamp"
        :class="timestampClass"
      >
        {{ formattedTime }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ChatBubble',
  props: {
    message: {
      type: String,
      required: true
    },
    isUser: {
      type: Boolean,
      default: false
    },
    timestamp: {
      type: [Date, String, Number],
      default: () => new Date()
    },
    userName: {
      type: String,
      default: 'User'
    }
  },
  setup(props) {
    const showTimestamp = ref(false)

    // Computed properties
    const messageTypeClass = computed(() => ({
      'message-user': props.isUser,
      'message-ai': !props.isUser
    }))

    const bubbleClass = computed(() => ({
      'bubble-user': props.isUser,
      'bubble-ai': !props.isUser
    }))

    const timestampClass = computed(() => ({
      'timestamp-user': props.isUser,
      'timestamp-ai': !props.isUser
    }))

    const userInitial = computed(() => {
      return props.userName.charAt(0).toUpperCase()
    })

    const formattedMessage = computed(() => {
      // Basic text formatting (can be enhanced later)
      return props.message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
        .replace(/\n/g, '<br>') // Line breaks
    })

    const formattedTime = computed(() => {
      const date = new Date(props.timestamp)
      return date.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    })

    return {
      showTimestamp,
      messageTypeClass,
      bubbleClass,
      timestampClass,
      userInitial,
      formattedMessage,
      formattedTime
    }
  }
}
</script>

<style scoped>
/* Chat Bubble Wrapper */
.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 16px;
  animation: bubbleAppear 0.3s ease-out;
}

.message-user {
  flex-direction: row-reverse;
  justify-content: flex-start;
}

.message-ai {
  flex-direction: row;
  justify-content: flex-start;
}

/* Avatar Styles */
.message-avatar {
  flex-shrink: 0;
  margin: 0 12px;
  align-self: flex-end;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  border: 2px solid #e2e8f0;
}

/* Message Bubble */
.message-bubble {
  position: relative;
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.message-bubble:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* User Message Bubble */
.bubble-user {
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  color: white;
  border-bottom-right-radius: 6px;
}

.bubble-user::before {
  content: '';
  position: absolute;
  bottom: 0;
  right: -6px;
  width: 0;
  height: 0;
  border: 6px solid transparent;
  border-left-color: #1976D2;
  border-bottom: none;
}

/* AI Message Bubble */
.bubble-ai {
  background: #f8fafc;
  color: #1a202c;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 6px;
}

.bubble-ai::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: -7px;
  width: 0;
  height: 0;
  border: 6px solid transparent;
  border-right-color: #e2e8f0;
  border-bottom: none;
}

.bubble-ai::after {
  content: '';
  position: absolute;
  bottom: 1px;
  left: -6px;
  width: 0;
  height: 0;
  border: 6px solid transparent;
  border-right-color: #f8fafc;
  border-bottom: none;
}

/* Message Content */
.message-content {
  position: relative;
}

.message-text {
  margin: 0;
  line-height: 1.4;
  font-size: 15px;
}

.bubble-user .message-text {
  color: white;
}

.bubble-ai .message-text {
  color: #2d3748;
}

/* Timestamp */
.message-timestamp {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #64748b;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  white-space: nowrap;
  z-index: 10;
  animation: fadeIn 0.2s ease-out;
}

.timestamp-user {
  right: calc(100% + 12px);
}

.timestamp-ai {
  left: calc(100% + 12px);
}

/* Animations */
@keyframes bubbleAppear {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-50%) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(-50%) scale(1);
  }
}

/* Mobile Responsive */
@media (max-width: 640px) {
  .message-bubble {
    max-width: 85%;
    padding: 10px 14px;
    font-size: 14px;
  }

  .message-avatar {
    margin: 0 8px;
  }

  .user-avatar,
  .ai-avatar {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .chat-bubble-wrapper {
    margin-bottom: 12px;
  }

  .message-timestamp {
    font-size: 11px;
    padding: 3px 6px;
  }
}

/* Accessibility - Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .message-bubble,
  .message-timestamp {
    animation: none;
    transition: none;
  }
  
  .message-bubble:hover {
    transform: none;
  }
}

/* Text Selection */
.message-text {
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .bubble-ai {
    border: 2px solid #000;
  }
  
  .bubble-user {
    border: 2px solid #fff;
  }
}
</style>
