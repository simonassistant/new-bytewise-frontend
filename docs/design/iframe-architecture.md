# 🏗️ iFrame-Compatible Architecture Design - Phase 2.1

**Date:** September 6, 2025  
**Phase:** 2.1 - iFrame Embeddable Architecture Design  
**Objective:** Create standalone chatbot component with postMessage communication

---

## 🎯 **Architecture Overview**

### **Design Philosophy: Standalone + Embeddable**
- **Self-contained**: All dependencies bundled, no external requirements
- **Communication**: PostMessage API for parent-child interaction
- **Responsive**: Dynamic sizing based on content and parent constraints
- **Secure**: Cross-origin safety with configurable CSP policies

---

## 🏛️ **1. Standalone Chatbot Component Architecture**

### **Component Hierarchy Design**

```
EmbeddableChatbot.vue (Root Component)
├── ChatbotCore.vue (Main Logic Container)
│   ├── ChatHeader.vue (Collapsible header with bot info)
│   ├── ChatMessages.vue (Message container)
│   │   └── ChatBubble.vue (Individual message - from your repo)
│   ├── ChatInput.vue (Input interface)
│   │   ├── InputModeToggle.vue (Hybrid voice+typing - from your repo)
│   │   ├── VoiceInput.vue (Voice recording interface)
│   │   └── TextInput.vue (Text input with auto-resize)
│   └── ChatFooter.vue (Optional branding/settings)
├── ConfigPanel.vue (Optional expandable settings)
└── NotificationOverlay.vue (Toast notifications)
```

### **Core Component Design**

#### **EmbeddableChatbot.vue (Root Container)**
```vue
<template>
  <div 
    class="embeddable-chatbot" 
    :class="themeClasses"
    :style="dynamicStyles"
    @resize="handleResize"
  >
    <!-- Loading State -->
    <div v-if="isInitializing" class="chatbot-loading">
      <div class="loading-spinner"></div>
      <p>Initializing AI Assistant...</p>
    </div>

    <!-- Main Chatbot Interface -->
    <ChatbotCore 
      v-else
      :config="chatbotConfig"
      :theme="theme"
      :size="containerSize"
      @message-sent="handleMessageSent"
      @resize-needed="handleResizeNeeded"
      @error="handleError"
    />

    <!-- Configuration Panel (expandable) -->
    <ConfigPanel 
      v-if="showConfig"
      :config="chatbotConfig"
      @config-updated="handleConfigUpdate"
      @close="showConfig = false"
    />

    <!-- Notification Overlay -->
    <NotificationOverlay :notifications="notifications" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useChatbotConfig } from '@/composables/useChatbotConfig';
import { usePostMessage } from '@/composables/usePostMessage';
import { useResizeObserver } from '@/composables/useResizeObserver';

// Props received from parent via postMessage
const props = defineProps({
  initialConfig: {
    type: Object,
    default: () => ({})
  }
});

// Reactive state
const isInitializing = ref(true);
const showConfig = ref(false);
const containerSize = ref({ width: 0, height: 0 });
const notifications = ref([]);

// Composables
const { chatbotConfig, updateConfig } = useChatbotConfig(props.initialConfig);
const { sendToParent, listenToParent } = usePostMessage();
const { observe, unobserve } = useResizeObserver(handleResize);

// Theme and styling
const theme = computed(() => chatbotConfig.value.theme || 'default');
const themeClasses = computed(() => [
  `theme-${theme.value}`,
  `size-${chatbotConfig.value.size || 'medium'}`
]);

const dynamicStyles = computed(() => ({
  '--primary-color': chatbotConfig.value.primaryColor || '#6366f1',
  '--secondary-color': chatbotConfig.value.secondaryColor || '#8b5cf6',
  '--border-radius': chatbotConfig.value.borderRadius || '12px',
  '--font-family': chatbotConfig.value.fontFamily || 'system-ui, sans-serif'
}));

// Lifecycle
onMounted(async () => {
  try {
    // Initialize chatbot with configuration
    await initializeChatbot();
    
    // Set up parent communication
    setupParentCommunication();
    
    // Start resize observer
    observe(document.querySelector('.embeddable-chatbot'));
    
    isInitializing.value = false;
    
    // Notify parent that chatbot is ready
    sendToParent('chatbot-ready', {
      initialSize: containerSize.value,
      config: chatbotConfig.value
    });
  } catch (error) {
    handleError('Initialization failed', error);
  }
});

onUnmounted(() => {
  unobserve();
  // Cleanup listeners
});

// Methods
async function initializeChatbot() {
  // Initialize AI connection, load bot config, etc.
  // Using merged logic from Bob's repository
}

function setupParentCommunication() {
  listenToParent('config-update', handleConfigFromParent);
  listenToParent('send-message', handleMessageFromParent);
  listenToParent('resize-container', handleResizeFromParent);
}

function handleResize(size) {
  containerSize.value = size;
  sendToParent('resize-request', size);
}

function handleMessageSent(message) {
  // Send message data to parent for logging/analytics
  sendToParent('message-sent', {
    message: message.content,
    timestamp: message.timestamp,
    tokens: message.metadata?.tokens
  });
}

function handleResizeNeeded(newSize) {
  sendToParent('resize-request', newSize);
}

function handleError(type, error) {
  console.error(`Chatbot Error [${type}]:`, error);
  sendToParent('error', { type, message: error.message });
}
</script>
```

---

## 📡 **2. PostMessage Communication System**

### **Communication Protocol Design**

#### **Message Structure Standard**
```typescript
interface ChatbotMessage {
  type: string;
  id: string;
  timestamp: number;
  data: any;
  origin?: string;
}

// Outbound Messages (Chatbot → Parent)
type OutboundMessageType = 
  | 'chatbot-ready'
  | 'resize-request' 
  | 'message-sent'
  | 'config-updated'
  | 'error'
  | 'analytics-event';

// Inbound Messages (Parent → Chatbot)  
type InboundMessageType =
  | 'config-update'
  | 'send-message'
  | 'resize-container'
  | 'theme-change'
  | 'reset-conversation';
```

#### **PostMessage Composable**
```javascript
// composables/usePostMessage.js
import { ref, onMounted, onUnmounted } from 'vue';

export function usePostMessage(allowedOrigins = ['*']) {
  const parentOrigin = ref(null);
  const messageQueue = ref([]);
  
  // Send message to parent
  function sendToParent(type, data) {
    const message = {
      type,
      id: generateId(),
      timestamp: Date.now(),
      data,
      source: 'bytewise-chatbot'
    };
    
    try {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(message, parentOrigin.value || '*');
      }
    } catch (error) {
      console.error('Failed to send message to parent:', error);
      // Queue message for retry
      messageQueue.value.push(message);
    }
  }
  
  // Listen for messages from parent
  function listenToParent(type, handler) {
    const messageHandler = (event) => {
      // Security check
      if (!isOriginAllowed(event.origin)) {
        console.warn('Message from unauthorized origin:', event.origin);
        return;
      }
      
      const message = event.data;
      if (message.type === type && message.target === 'bytewise-chatbot') {
        parentOrigin.value = event.origin; // Store parent origin
        handler(message.data, message);
      }
    };
    
    window.addEventListener('message', messageHandler);
    
    // Return cleanup function
    return () => window.removeEventListener('message', messageHandler);
  }
  
  function isOriginAllowed(origin) {
    if (allowedOrigins.includes('*')) return true;
    return allowedOrigins.includes(origin);
  }
  
  function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  
  return {
    sendToParent,
    listenToParent,
    parentOrigin,
    messageQueue
  };
}
```

### **Communication Examples**

#### **Initialization Handshake**
```javascript
// 1. Parent sends initial config
parent.postMessage({
  type: 'config-update',
  target: 'bytewise-chatbot',
  data: {
    apiKey: 'xxx',
    systemPrompt: 'You are a helpful assistant...',
    theme: 'corporate',
    primaryColor: '#0066cc',
    allowedDomains: ['company.com']
  }
}, '*');

// 2. Chatbot responds when ready
// (sent from chatbot iframe)
{
  type: 'chatbot-ready',
  source: 'bytewise-chatbot',
  data: {
    initialSize: { width: 400, height: 600 },
    supportedFeatures: ['voice', 'typing', 'email-export']
  }
}
```

#### **Dynamic Resizing Communication**
```javascript
// Chatbot requests resize
{
  type: 'resize-request',
  data: {
    width: 450,
    height: 800,
    reason: 'content-overflow'
  }
}

// Parent acknowledges resize
{
  type: 'resize-container',
  target: 'bytewise-chatbot', 
  data: {
    width: 450,
    height: 700, // Parent may constrain size
    approved: true
  }
}
```

---

## 📐 **3. Responsive iFrame Sizing Mechanism**

### **Dynamic Sizing Strategy**

#### **Size Calculation Logic**
```javascript
// composables/useResizeObserver.js
import { ref, nextTick } from 'vue';

export function useResponsiveSizing() {
  const containerSize = ref({ width: 0, height: 0 });
  const contentSize = ref({ width: 0, height: 0 });
  const parentConstraints = ref({ maxWidth: Infinity, maxHeight: Infinity });
  
  // Calculate optimal size based on content and constraints
  function calculateOptimalSize() {
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input');
    const chatHeader = document.querySelector('.chat-header');
    
    if (!chatMessages || !chatInput || !chatHeader) return;
    
    // Calculate content height
    const headerHeight = chatHeader.offsetHeight;
    const inputHeight = chatInput.offsetHeight;
    const messagesHeight = Math.min(
      chatMessages.scrollHeight,
      600 // Max messages height
    );
    
    const totalHeight = headerHeight + messagesHeight + inputHeight + 32; // padding
    const minWidth = 320; // Mobile minimum
    const preferredWidth = 400;
    
    const optimalSize = {
      width: Math.max(minWidth, Math.min(preferredWidth, parentConstraints.value.maxWidth)),
      height: Math.min(totalHeight, parentConstraints.value.maxHeight)
    };
    
    return optimalSize;
  }
  
  // Responsive breakpoints
  const sizeVariants = {
    compact: { width: 300, height: 400 },
    normal: { width: 400, height: 600 },
    expanded: { width: 500, height: 700 }
  };
  
  function getResponsiveVariant(containerWidth) {
    if (containerWidth < 350) return 'compact';
    if (containerWidth < 450) return 'normal';
    return 'expanded';
  }
  
  return {
    containerSize,
    contentSize,
    calculateOptimalSize,
    getResponsiveVariant,
    sizeVariants
  };
}
```

#### **Auto-Resize Implementation**
```vue
<!-- ChatbotCore.vue -->
<template>
  <div 
    class="chatbot-core"
    :class="sizeVariant"
    @content-change="handleContentChange"
  >
    <!-- Chatbot content -->
  </div>
</template>

<script setup>
import { watch, nextTick } from 'vue';
import { useResponsiveSizing } from '@/composables/useResponsiveSizing';

const emit = defineEmits(['resize-needed']);

const { calculateOptimalSize, getResponsiveVariant } = useResponsiveSizing();

// Watch for content changes that might require resize
watch(() => chatHistory.value.length, async () => {
  await nextTick();
  const newSize = calculateOptimalSize();
  emit('resize-needed', newSize);
});

// Handle input expansion (e.g., multi-line text)
function handleInputExpansion(newInputHeight) {
  const currentSize = calculateOptimalSize();
  const newSize = {
    ...currentSize,
    height: currentSize.height + (newInputHeight - 60) // 60px base input height
  };
  emit('resize-needed', newSize);
}
</script>
```

---

## 🔒 **4. Cross-Origin Security Considerations**

### **Security Architecture**

#### **Content Security Policy (CSP)**
```html
<!-- iframe-host.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Strict CSP for iframe content -->
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline';
    style-src 'self' 'unsafe-inline';
    connect-src 'self' https://api.openrouter.ai https://*.hkbu.edu.hk;
    img-src 'self' data: https:;
    font-src 'self' data:;
    frame-ancestors 'self' ${ALLOWED_PARENT_ORIGINS};
    form-action 'none';
    base-uri 'self';
  ">
  
  <title>ByteWise AI Chatbot</title>
</head>
<body>
  <div id="chatbot-app"></div>
  <script src="/assets/chatbot.js"></script>
</body>
</html>
```

#### **Origin Validation System**
```javascript
// utils/securityValidator.js
export class SecurityValidator {
  constructor(allowedOrigins = []) {
    this.allowedOrigins = new Set(allowedOrigins);
    this.trustedDomains = new Set(['localhost', '127.0.0.1']); // Dev domains
  }
  
  validateOrigin(origin) {
    if (this.allowedOrigins.has('*')) return true;
    
    try {
      const url = new URL(origin);
      const domain = url.hostname;
      
      // Check exact match
      if (this.allowedOrigins.has(origin)) return true;
      
      // Check domain wildcards
      for (const allowed of this.allowedOrigins) {
        if (allowed.startsWith('*.') && domain.endsWith(allowed.slice(2))) {
          return true;
        }
      }
      
      // Development mode
      if (process.env.NODE_ENV === 'development' && this.trustedDomains.has(domain)) {
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Invalid origin URL:', origin);
      return false;
    }
  }
  
  sanitizeMessage(message) {
    // Sanitize incoming postMessage data
    if (typeof message !== 'object' || !message.type) {
      throw new Error('Invalid message format');
    }
    
    // Remove potentially dangerous properties
    const sanitized = {
      type: String(message.type),
      data: this.sanitizeData(message.data),
      id: String(message.id || ''),
      timestamp: Number(message.timestamp || Date.now())
    };
    
    return sanitized;
  }
  
  sanitizeData(data) {
    if (typeof data !== 'object') return data;
    
    // Remove script tags, event handlers, etc.
    const sanitized = {};
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        sanitized[key] = value.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
      } else if (typeof value === 'object') {
        sanitized[key] = this.sanitizeData(value);
      } else {
        sanitized[key] = value;
      }
    }
    
    return sanitized;
  }
}
```

#### **Secure API Key Handling**
```javascript
// composables/useSecureConfig.js
import { ref, computed } from 'vue';
import { SecurityValidator } from '@/utils/securityValidator';

export function useSecureConfig(initialConfig = {}) {
  const rawConfig = ref(initialConfig);
  const validator = new SecurityValidator(initialConfig.allowedOrigins);
  
  // Secure configuration with validation
  const secureConfig = computed(() => {
    const config = { ...rawConfig.value };
    
    // Never expose API keys in logs or errors
    if (config.apiKey) {
      config._hasApiKey = true;
      // Store encrypted or hashed version only
      config._apiKeyHash = btoa(config.apiKey.slice(0, 8));
      delete config.apiKey; // Remove from reactive state
    }
    
    return config;
  });
  
  // API key accessor with validation
  function getApiKey() {
    const key = rawConfig.value.apiKey;
    if (!key || typeof key !== 'string') {
      throw new Error('Invalid API key configuration');
    }
    return key;
  }
  
  function updateConfig(newConfig, origin) {
    // Validate origin
    if (!validator.validateOrigin(origin)) {
      throw new Error(`Configuration update from unauthorized origin: ${origin}`);
    }
    
    // Sanitize configuration
    const sanitized = validator.sanitizeData(newConfig);
    rawConfig.value = { ...rawConfig.value, ...sanitized };
  }
  
  return {
    secureConfig,
    getApiKey,
    updateConfig,
    validator
  };
}
```

### **Sandbox Configuration**
```html
<!-- Parent page iframe embedding -->
<iframe 
  src="https://chatbot.bytewise.ai/embed"
  sandbox="allow-scripts allow-same-origin allow-forms"
  allow="microphone; camera"
  referrerpolicy="strict-origin-when-cross-origin"
  loading="lazy"
  width="400"
  height="600"
  style="border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
>
</iframe>
```

---

## 🏗️ **Implementation Architecture Summary**

### **Component Structure:**
```
src/
├── components/
│   ├── embeddable/
│   │   ├── EmbeddableChatbot.vue (Root)
│   │   ├── ChatbotCore.vue (Main logic)
│   │   └── ConfigPanel.vue (Settings)
│   ├── chat/ (From your repo)
│   │   ├── ChatBubble.vue
│   │   ├── InputModeToggle.vue
│   │   └── ChatMessages.vue
│   └── ui/
│       └── NotificationOverlay.vue
├── composables/
│   ├── usePostMessage.js (Communication)
│   ├── useChatbotConfig.js (Config management)
│   ├── useResponsiveSizing.js (Dynamic sizing)
│   └── useSecureConfig.js (Security)
├── utils/
│   ├── securityValidator.js
│   └── messageProtocol.js
└── styles/
    ├── embeddable.scss (iframe-specific styles)
    └── themes/ (Customizable themes)
```

### **Build Configuration:**
```javascript
// vite.config.js - iframe-specific build
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        chatbot: 'src/embeddable/main.js'
      },
      output: {
        entryFileNames: 'assets/chatbot.[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    }
  },
  define: {
    'process.env.IFRAME_MODE': true
  }
});
```

This architecture provides a robust foundation for embeddable chatbot deployment with security, responsiveness, and seamless parent-child communication! 🚀
