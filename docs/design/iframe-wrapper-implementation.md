# 🖼️ iFrame Wrapper & Parent Communication - Phase 2.2

**Date:** September 6, 2025  
**Phase:** 2.2 - iFrame Host Implementation & Communication  
**Objective:** Create complete embedding system with configuration passing and event handling

---

## 🏗️ **1. iFrame Host HTML Template**

### **Primary Host Template**

#### **iframe-host.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Security Headers -->
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' 'unsafe-eval';
    style-src 'self' 'unsafe-inline';
    connect-src 'self' 
      https://api.openrouter.ai 
      https://*.hkbu.edu.hk 
      https://new-bytewise-backend-production-8c33.up.railway.app 
      https://smartlessons-production.up.railway.app
      wss://*.railway.app;
    img-src 'self' data: https:;
    font-src 'self' data: https://fonts.googleapis.com https://fonts.gstatic.com;
    media-src 'self' blob:;
    worker-src 'self' blob:;
    frame-ancestors ALLOWED_ORIGINS_PLACEHOLDER;
    form-action 'none';
    base-uri 'self';
  ">
  
  <!-- Prevent clickjacking -->
  <meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
  
  <!-- Referrer policy -->
  <meta name="referrer" content="strict-origin-when-cross-origin">
  
  <title>ByteWise AI Chatbot</title>
  
  <!-- Preload critical resources -->
  <link rel="preload" href="/assets/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preconnect" href="https://api.openrouter.ai">
  
  <!-- Inline critical CSS to prevent FOUC -->
  <style>
    /* Critical CSS for initial load */
    * { box-sizing: border-box; }
    
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: system-ui, -apple-system, sans-serif;
      background: transparent;
      overflow: hidden;
    }
    
    #chatbot-app {
      width: 100%;
      height: 100%;
      position: relative;
    }
    
    .chatbot-loading {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 2rem;
      border-radius: 12px;
    }
    
    .loading-spinner {
      width: 40px;
      height: 40px;
      border: 3px solid rgba(255,255,255,0.3);
      border-top: 3px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin-bottom: 1rem;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .error-state {
      padding: 1rem;
      background: #fee;
      border: 1px solid #fcc;
      border-radius: 8px;
      color: #c33;
      text-align: center;
    }
    
    /* Responsive base styles */
    @media (max-width: 640px) {
      .chatbot-loading {
        padding: 1rem;
        font-size: 0.9rem;
      }
    }
  </style>
</head>
<body>
  <!-- Main application container -->
  <div id="chatbot-app">
    <!-- Initial loading state -->
    <div class="chatbot-loading" id="initial-loader">
      <div class="loading-spinner"></div>
      <p>Initializing ByteWise AI...</p>
      <small>Connecting to AI services...</small>
    </div>
  </div>
  
  <!-- Configuration script (populated by server) -->
  <script id="chatbot-config">
    window.CHATBOT_CONFIG = {
      apiEndpoint: 'ENDPOINT_PLACEHOLDER',
      allowedOrigins: 'ORIGINS_PLACEHOLDER',
      version: 'VERSION_PLACEHOLDER',
      buildTime: 'BUILD_TIME_PLACEHOLDER',
      features: {
        voice: true,
        typing: true,
        email: true,
        themes: true
      }
    };
  </script>
  
  <!-- Error handling script (loads immediately) -->
  <script>
    window.onerror = function(msg, url, lineNo, columnNo, error) {
      console.error('Chatbot Error:', { msg, url, lineNo, columnNo, error });
      
      // Send error to parent
      if (window.parent !== window) {
        window.parent.postMessage({
          type: 'error',
          source: 'bytewise-chatbot',
          data: {
            message: msg,
            file: url,
            line: lineNo,
            column: columnNo,
            stack: error?.stack
          }
        }, '*');
      }
      
      // Show error UI
      document.getElementById('chatbot-app').innerHTML = 
        '<div class="error-state">' +
        '<h3>⚠️ Chatbot Error</h3>' +
        '<p>Unable to load the AI assistant. Please refresh or contact support.</p>' +
        '<details><summary>Technical Details</summary><pre>' + msg + '</pre></details>' +
        '</div>';
      
      return true;
    };
    
    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', function(event) {
      console.error('Unhandled promise rejection:', event.reason);
      window.onerror(event.reason.message || 'Promise rejection', '', 0, 0, event.reason);
    });
  </script>
  
  <!-- Main chatbot application (loaded after DOM ready) -->
  <script defer src="/assets/chatbot.js?v=BUILD_HASH_PLACEHOLDER"></script>
</body>
</html>
```

### **Development Version**
#### **iframe-host.dev.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ByteWise AI Chatbot - Development</title>
  
  <!-- Development-specific meta -->
  <meta name="environment" content="development">
  
  <!-- Relaxed CSP for development -->
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self' 'unsafe-inline' 'unsafe-eval';
    connect-src 'self' ws://localhost:* http://localhost:* https://api.openrouter.ai;
    img-src 'self' data: https:;
    font-src 'self' data: https:;
    frame-ancestors 'self' http://localhost:* https://localhost:*;
  ">
  
  <!-- Development styles (not inlined) -->
  <link rel="stylesheet" href="/src/styles/embeddable.scss">
</head>
<body>
  <div id="chatbot-app">
    <div class="chatbot-loading" id="initial-loader">
      <div class="loading-spinner"></div>
      <p>Development Mode</p>
      <small>Hot reload enabled</small>
    </div>
  </div>
  
  <script>
    window.CHATBOT_CONFIG = {
      apiEndpoint: 'http://localhost:5000/api',
      allowedOrigins: ['*'],
      version: 'dev',
      buildTime: new Date().toISOString(),
      debug: true,
      features: {
        voice: true,
        typing: true,
        email: true,
        themes: true,
        devTools: true
      }
    };
  </script>
  
  <!-- Vite development server -->
  <script type="module" src="/src/embeddable/main.js"></script>
</body>
</html>
```

---

## ⚙️ **2. Configuration Passing Mechanism**

### **Configuration Manager**

#### **ConfigurationManager.js**
```javascript
// utils/ConfigurationManager.js
export class ConfigurationManager {
  constructor() {
    this.config = new Map();
    this.validators = new Map();
    this.observers = new Set();
    this.initializeDefaults();
  }
  
  initializeDefaults() {
    this.setDefaults({
      // API Configuration
      apiProvider: 'hkbu', // hkbu, openrouter, custom
      apiKey: null,
      apiEndpoint: null,
      model: 'gpt-4.1-mini',
      
      // UI Configuration
      theme: 'default', // default, corporate, minimal, dark
      primaryColor: '#6366f1',
      secondaryColor: '#8b5cf6',
      borderRadius: '12px',
      fontFamily: 'system-ui, sans-serif',
      size: 'normal', // compact, normal, expanded
      
      // Behavior Configuration
      systemPrompt: 'You are a helpful AI assistant.',
      welcomeMessage: 'Hello! How can I help you today?',
      enableVoice: true,
      enableTyping: true,
      enableEmail: false,
      autoResize: true,
      
      // Security Configuration
      allowedOrigins: ['*'],
      maxMessageLength: 4000,
      rateLimitMessages: 60, // per minute
      
      // Feature Flags
      features: {
        contextMemory: true,
        tokenTracking: true,
        exportConversation: true,
        customPrompts: false,
        analytics: false
      }
    });
  }
  
  setDefaults(defaults) {
    for (const [key, value] of Object.entries(defaults)) {
      if (!this.config.has(key)) {
        this.config.set(key, value);
      }
    }
  }
  
  // Configuration validation
  addValidator(key, validatorFn) {
    this.validators.set(key, validatorFn);
  }
  
  setupValidators() {
    // API Key validation
    this.addValidator('apiKey', (value) => {
      if (!value) return { valid: false, error: 'API key is required' };
      if (typeof value !== 'string') return { valid: false, error: 'API key must be string' };
      if (value.length < 10) return { valid: false, error: 'API key too short' };
      return { valid: true };
    });
    
    // Theme validation
    this.addValidator('theme', (value) => {
      const validThemes = ['default', 'corporate', 'minimal', 'dark'];
      if (!validThemes.includes(value)) {
        return { valid: false, error: `Theme must be one of: ${validThemes.join(', ')}` };
      }
      return { valid: true };
    });
    
    // Color validation
    this.addValidator('primaryColor', (value) => {
      const colorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
      if (!colorRegex.test(value)) {
        return { valid: false, error: 'Color must be valid hex code' };
      }
      return { valid: true };
    });
    
    // System prompt validation
    this.addValidator('systemPrompt', (value) => {
      if (!value || typeof value !== 'string') {
        return { valid: false, error: 'System prompt must be non-empty string' };
      }
      if (value.length > 2000) {
        return { valid: false, error: 'System prompt too long (max 2000 chars)' };
      }
      return { valid: true };
    });
  }
  
  // Update configuration with validation
  updateConfig(updates, origin = null) {
    const validationErrors = [];
    const validUpdates = {};
    
    for (const [key, value] of Object.entries(updates)) {
      const validator = this.validators.get(key);
      
      if (validator) {
        const validation = validator(value);
        if (!validation.valid) {
          validationErrors.push(`${key}: ${validation.error}`);
          continue;
        }
      }
      
      validUpdates[key] = value;
      this.config.set(key, value);
    }
    
    if (validationErrors.length > 0) {
      throw new Error(`Configuration validation failed:\n${validationErrors.join('\n')}`);
    }
    
    // Notify observers
    this.notifyObservers(validUpdates, origin);
    
    return validUpdates;
  }
  
  // Get configuration value
  get(key, fallback = undefined) {
    return this.config.has(key) ? this.config.get(key) : fallback;
  }
  
  // Get all configuration
  getAll() {
    return Object.fromEntries(this.config);
  }
  
  // Observe configuration changes
  observe(callback) {
    this.observers.add(callback);
    return () => this.observers.delete(callback);
  }
  
  notifyObservers(changes, origin) {
    for (const observer of this.observers) {
      try {
        observer(changes, origin);
      } catch (error) {
        console.error('Configuration observer error:', error);
      }
    }
  }
  
  // Export/Import configuration
  exportConfig() {
    const config = this.getAll();
    // Remove sensitive data
    const sanitized = { ...config };
    if (sanitized.apiKey) {
      sanitized.apiKey = '***REDACTED***';
    }
    return JSON.stringify(sanitized, null, 2);
  }
  
  importConfig(configJson, origin = null) {
    try {
      const config = JSON.parse(configJson);
      return this.updateConfig(config, origin);
    } catch (error) {
      throw new Error(`Invalid configuration JSON: ${error.message}`);
    }
  }
}
```

### **Configuration Composable**

#### **useChatbotConfig.js**
```javascript
// composables/useChatbotConfig.js
import { ref, computed, watch } from 'vue';
import { ConfigurationManager } from '@/utils/ConfigurationManager';

let globalConfigManager = null;

export function useChatbotConfig(initialConfig = {}) {
  // Singleton pattern for configuration
  if (!globalConfigManager) {
    globalConfigManager = new ConfigurationManager();
    globalConfigManager.setupValidators();
  }
  
  const configManager = globalConfigManager;
  const isLoading = ref(false);
  const errors = ref([]);
  
  // Initialize with provided config
  if (Object.keys(initialConfig).length > 0) {
    try {
      configManager.updateConfig(initialConfig);
    } catch (error) {
      errors.value.push(error.message);
      console.error('Initial config validation failed:', error);
    }
  }
  
  // Reactive configuration
  const config = ref(configManager.getAll());
  
  // Computed derived values
  const themeConfig = computed(() => ({
    '--primary-color': config.value.primaryColor,
    '--secondary-color': config.value.secondaryColor,
    '--border-radius': config.value.borderRadius,
    '--font-family': config.value.fontFamily
  }));
  
  const apiConfig = computed(() => ({
    provider: config.value.apiProvider,
    endpoint: config.value.apiEndpoint,
    model: config.value.model,
    hasApiKey: !!config.value.apiKey
  }));
  
  const uiConfig = computed(() => ({
    theme: config.value.theme,
    size: config.value.size,
    enableVoice: config.value.enableVoice,
    enableTyping: config.value.enableTyping,
    enableEmail: config.value.enableEmail,
    autoResize: config.value.autoResize
  }));
  
  // Watch for configuration changes and sync
  const unsubscribe = configManager.observe((changes, origin) => {
    config.value = configManager.getAll();
    console.log('Configuration updated:', changes, 'from:', origin);
  });
  
  // Methods
  async function updateConfig(updates, origin = 'local') {
    isLoading.value = true;
    errors.value = [];
    
    try {
      const validUpdates = configManager.updateConfig(updates, origin);
      return validUpdates;
    } catch (error) {
      errors.value.push(error.message);
      throw error;
    } finally {
      isLoading.value = false;
    }
  }
  
  function resetConfig() {
    configManager.initializeDefaults();
    config.value = configManager.getAll();
  }
  
  function getApiKey() {
    return configManager.get('apiKey');
  }
  
  function exportConfig() {
    return configManager.exportConfig();
  }
  
  async function importConfig(configJson, origin = 'import') {
    return updateConfig(JSON.parse(configJson), origin);
  }
  
  // Theme utilities
  function applyTheme() {
    const root = document.documentElement;
    const theme = themeConfig.value;
    
    for (const [property, value] of Object.entries(theme)) {
      root.style.setProperty(property, value);
    }
    
    // Add theme class to body
    document.body.className = document.body.className
      .replace(/theme-\w+/g, '')
      .concat(` theme-${config.value.theme}`);
  }
  
  // Auto-apply theme when it changes
  watch(() => config.value.theme, applyTheme, { immediate: true });
  watch(themeConfig, applyTheme, { deep: true });
  
  // Cleanup
  function destroy() {
    unsubscribe();
  }
  
  return {
    config: computed(() => config.value),
    themeConfig,
    apiConfig,
    uiConfig,
    isLoading: computed(() => isLoading.value),
    errors: computed(() => errors.value),
    
    // Methods
    updateConfig,
    resetConfig,
    getApiKey,
    exportConfig,
    importConfig,
    applyTheme,
    destroy
  };
}
```

---

## 🔄 **3. Event Bubbling System**

### **Event Manager**

#### **EventManager.js**
```javascript
// utils/EventManager.js
export class EventManager {
  constructor() {
    this.listeners = new Map();
    this.eventQueue = [];
    this.isProcessingQueue = false;
    this.parentOrigin = null;
    this.childOrigins = new Set();
  }
  
  // Initialize event system
  initialize(allowedOrigins = ['*']) {
    this.allowedOrigins = new Set(allowedOrigins);
    this.setupMessageListener();
    this.setupParentDetection();
  }
  
  setupMessageListener() {
    window.addEventListener('message', (event) => {
      this.handleIncomingMessage(event);
    });
  }
  
  setupParentDetection() {
    // Detect if we're in an iframe
    if (window.parent !== window) {
      // Send handshake to parent
      this.sendToParent('chatbot-handshake', {
        timestamp: Date.now(),
        url: window.location.href,
        capabilities: this.getCapabilities()
      });
    }
  }
  
  getCapabilities() {
    return {
      voice: 'mediaDevices' in navigator,
      notifications: 'Notification' in window,
      storage: 'localStorage' in window,
      webgl: this.hasWebGL(),
      touch: 'ontouchstart' in window
    };
  }
  
  hasWebGL() {
    try {
      const canvas = document.createElement('canvas');
      return !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
    } catch (e) {
      return false;
    }
  }
  
  // Message validation
  validateMessage(event) {
    // Origin validation
    if (!this.allowedOrigins.has('*') && !this.allowedOrigins.has(event.origin)) {
      console.warn('Message from unauthorized origin:', event.origin);
      return false;
    }
    
    // Message structure validation
    const message = event.data;
    if (!message || typeof message !== 'object' || !message.type) {
      console.warn('Invalid message format:', message);
      return false;
    }
    
    return true;
  }
  
  // Handle incoming messages
  handleIncomingMessage(event) {
    if (!this.validateMessage(event)) return;
    
    const message = event.data;
    const { type, data, source, target, id } = message;
    
    // Store parent origin on first valid message
    if (!this.parentOrigin && source !== 'bytewise-chatbot') {
      this.parentOrigin = event.origin;
    }
    
    // Route message based on target
    if (target === 'bytewise-chatbot' || !target) {
      this.processMessage(type, data, {
        ...message,
        origin: event.origin,
        timestamp: Date.now()
      });
    }
    
    // Send acknowledgment for important messages
    if (message.requiresAck) {
      this.sendToParent('message-ack', {
        originalId: id,
        status: 'received',
        timestamp: Date.now()
      });
    }
  }
  
  // Process message by type
  processMessage(type, data, metadata) {
    const handlers = this.listeners.get(type) || [];
    
    if (handlers.length === 0) {
      console.warn(`No handlers for message type: ${type}`);
      return;
    }
    
    // Execute handlers
    for (const handler of handlers) {
      try {
        handler(data, metadata);
      } catch (error) {
        console.error(`Handler error for ${type}:`, error);
        this.sendError(`Handler error for ${type}: ${error.message}`);
      }
    }
  }
  
  // Send message to parent
  sendToParent(type, data, options = {}) {
    const message = {
      type,
      data,
      source: 'bytewise-chatbot',
      id: this.generateId(),
      timestamp: Date.now(),
      ...options
    };
    
    if (window.parent && window.parent !== window) {
      try {
        window.parent.postMessage(message, this.parentOrigin || '*');
      } catch (error) {
        console.error('Failed to send message to parent:', error);
        this.queueMessage(message);
      }
    } else {
      console.warn('No parent window found for message:', message);
    }
  }
  
  // Send message to specific child (if we're the parent)
  sendToChild(iframe, type, data, options = {}) {
    const message = {
      type,
      data,
      target: 'bytewise-chatbot',
      source: 'parent-window',
      id: this.generateId(),
      timestamp: Date.now(),
      ...options
    };
    
    if (iframe && iframe.contentWindow) {
      try {
        iframe.contentWindow.postMessage(message, '*');
      } catch (error) {
        console.error('Failed to send message to child:', error);
      }
    }
  }
  
  // Event registration
  on(type, handler) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, []);
    }
    this.listeners.get(type).push(handler);
    
    // Return unsubscribe function
    return () => {
      const handlers = this.listeners.get(type) || [];
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    };
  }
  
  // Remove event listener
  off(type, handler) {
    const handlers = this.listeners.get(type) || [];
    const index = handlers.indexOf(handler);
    if (index > -1) {
      handlers.splice(index, 1);
    }
  }
  
  // Send error to parent
  sendError(message, details = {}) {
    this.sendToParent('error', {
      message,
      details,
      timestamp: Date.now(),
      stack: new Error().stack
    });
  }
  
  // Queue messages for retry
  queueMessage(message) {
    this.eventQueue.push(message);
    this.processQueue();
  }
  
  async processQueue() {
    if (this.isProcessingQueue || this.eventQueue.length === 0) return;
    
    this.isProcessingQueue = true;
    
    while (this.eventQueue.length > 0) {
      const message = this.eventQueue.shift();
      
      try {
        if (window.parent && window.parent !== window) {
          window.parent.postMessage(message, this.parentOrigin || '*');
        }
        
        // Wait a bit before next message
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error('Failed to send queued message:', error);
        // Re-queue if it's an important message
        if (message.important) {
          this.eventQueue.push(message);
        }
        break;
      }
    }
    
    this.isProcessingQueue = false;
  }
  
  // Utility methods
  generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  
  // Cleanup
  destroy() {
    this.listeners.clear();
    this.eventQueue = [];
    // Remove window listener if needed
  }
}

// Global singleton
let globalEventManager = null;

export function getEventManager() {
  if (!globalEventManager) {
    globalEventManager = new EventManager();
  }
  return globalEventManager;
}
```

### **Event Composable**

#### **useEventBubbling.js**
```javascript
// composables/useEventBubbling.js
import { onMounted, onUnmounted } from 'vue';
import { getEventManager } from '@/utils/EventManager';

export function useEventBubbling() {
  const eventManager = getEventManager();
  const unsubscribers = [];
  
  onMounted(() => {
    eventManager.initialize();
  });
  
  onUnmounted(() => {
    // Clean up all event listeners
    unsubscribers.forEach(unsubscribe => unsubscribe());
    unsubscribers.length = 0;
  });
  
  // Listen to parent messages
  function listenToParent(eventType, handler) {
    const unsubscribe = eventManager.on(eventType, handler);
    unsubscribers.push(unsubscribe);
    return unsubscribe;
  }
  
  // Send message to parent
  function sendToParent(eventType, data, options = {}) {
    eventManager.sendToParent(eventType, data, options);
  }
  
  // Send message to child iframe
  function sendToChild(iframe, eventType, data, options = {}) {
    eventManager.sendToChild(iframe, eventType, data, options);
  }
  
  // Register standard chatbot events
  function registerStandardEvents() {
    // Configuration updates from parent
    listenToParent('config-update', (config, metadata) => {
      console.log('Received config update:', config);
      // Handle configuration update
      window.dispatchEvent(new CustomEvent('chatbot-config-update', {
        detail: { config, metadata }
      }));
    });
    
    // Resize requests from parent
    listenToParent('resize-container', (sizeData, metadata) => {
      console.log('Received resize request:', sizeData);
      window.dispatchEvent(new CustomEvent('chatbot-resize', {
        detail: { size: sizeData, metadata }
      }));
    });
    
    // Message injection from parent
    listenToParent('inject-message', (messageData, metadata) => {
      console.log('Received message injection:', messageData);
      window.dispatchEvent(new CustomEvent('chatbot-inject-message', {
        detail: { message: messageData, metadata }
      }));
    });
    
    // Theme changes from parent
    listenToParent('theme-update', (themeData, metadata) => {
      console.log('Received theme update:', themeData);
      window.dispatchEvent(new CustomEvent('chatbot-theme-update', {
        detail: { theme: themeData, metadata }
      }));
    });
  }
  
  // Send standard events to parent
  function sendReadyEvent(data = {}) {
    sendToParent('chatbot-ready', {
      capabilities: eventManager.getCapabilities(),
      timestamp: Date.now(),
      ...data
    });
  }
  
  function sendResizeRequest(size, reason = 'content-change') {
    sendToParent('resize-request', {
      width: size.width,
      height: size.height,
      reason,
      timestamp: Date.now()
    });
  }
  
  function sendMessageEvent(message) {
    sendToParent('message-sent', {
      content: message.content,
      role: message.role,
      timestamp: message.timestamp,
      metadata: message.metadata
    });
  }
  
  function sendErrorEvent(error, context = {}) {
    sendToParent('error', {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now()
    });
  }
  
  function sendAnalyticsEvent(eventName, data = {}) {
    sendToParent('analytics', {
      event: eventName,
      data,
      timestamp: Date.now(),
      url: window.location.href
    });
  }
  
  return {
    // Core methods
    listenToParent,
    sendToParent,
    sendToChild,
    
    // Standard event setup
    registerStandardEvents,
    
    // Convenience methods
    sendReadyEvent,
    sendResizeRequest,
    sendMessageEvent,
    sendErrorEvent,
    sendAnalyticsEvent
  };
}
```

---

## 🔒 **4. Sandbox Security Settings**

### **Security Configuration**

#### **sandbox-config.js**
```javascript
// config/sandbox-config.js
export const SANDBOX_SETTINGS = {
  // Production iframe sandbox attributes
  production: [
    'allow-scripts',           // Required for Vue.js to run
    'allow-same-origin',       // Required for API calls
    'allow-forms',            // Required for input handling
    'allow-modals',           // For confirmation dialogs
    'allow-popups-to-escape-sandbox', // For external links
    'allow-storage-access-by-user-activation' // For settings persistence
  ],
  
  // Development iframe sandbox attributes (more permissive)
  development: [
    'allow-scripts',
    'allow-same-origin', 
    'allow-forms',
    'allow-modals',
    'allow-popups',
    'allow-downloads', // For dev tools
    'allow-storage-access-by-user-activation'
  ],
  
  // Feature-specific permissions
  permissions: {
    voice: 'microphone',
    camera: 'camera', // Future video chat
    notifications: 'notifications',
    location: 'geolocation', // For location-aware responses
    storage: 'storage-access'
  }
};

export const CSP_POLICIES = {
  production: {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    'connect-src': [
      "'self'",
      "https://api.openrouter.ai",
      "https://*.hkbu.edu.hk",
      "https://*.railway.app",
      "wss://*.railway.app"
    ],
    'img-src': ["'self'", "data:", "https:"],
    'font-src': ["'self'", "data:", "https://fonts.gstatic.com"],
    'media-src': ["'self'", "blob:"],
    'worker-src': ["'self'", "blob:"],
    'frame-ancestors': "REPLACE_WITH_ALLOWED_ORIGINS",
    'form-action': ["'none'"],
    'base-uri': ["'self'"]
  },
  
  development: {
    'default-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
    'connect-src': ["'self'", "ws://localhost:*", "http://localhost:*", "https:"],
    'img-src': ["'self'", "data:", "https:", "http:"],
    'font-src': ["'self'", "data:", "https:", "http:"],
    'frame-ancestors': ["'self'", "http://localhost:*", "https://localhost:*"]
  }
};

// Generate CSP string
export function generateCSP(policies, environment = 'production') {
  const policy = policies[environment];
  const cspString = Object.entries(policy)
    .map(([directive, sources]) => {
      if (Array.isArray(sources)) {
        return `${directive} ${sources.join(' ')}`;
      }
      return `${directive} ${sources}`;
    })
    .join('; ');
  
  return cspString;
}

// Iframe generator with security settings
export function generateSecureIframe(src, options = {}) {
  const {
    width = 400,
    height = 600,
    sandbox = SANDBOX_SETTINGS.production,
    allow = Object.values(SANDBOX_SETTINGS.permissions).join('; '),
    referrerPolicy = 'strict-origin-when-cross-origin',
    loading = 'lazy',
    className = 'bytewise-chatbot-iframe',
    style = {}
  } = options;
  
  const iframe = document.createElement('iframe');
  
  // Basic attributes
  iframe.src = src;
  iframe.width = width;
  iframe.height = height;
  iframe.className = className;
  iframe.loading = loading;
  iframe.referrerPolicy = referrerPolicy;
  
  // Security attributes
  iframe.sandbox = sandbox.join(' ');
  iframe.allow = allow;
  
  // Styling
  const defaultStyles = {
    border: 'none',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    backgroundColor: '#fff'
  };
  
  Object.assign(iframe.style, defaultStyles, style);
  
  return iframe;
}
```

### **Parent Integration Helper**

#### **chatbot-embedder.js**
```javascript
// dist/chatbot-embedder.js - For parent websites
(function(window) {
  'use strict';
  
  class ByteWiseChatbot {
    constructor(container, config = {}) {
      this.container = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
      
      if (!this.container) {
        throw new Error('Container element not found');
      }
      
      this.config = {
        // Default configuration
        src: 'https://chatbot.bytewise.ai/embed',
        width: 400,
        height: 600,
        theme: 'default',
        apiProvider: 'hkbu',
        enableVoice: true,
        enableTyping: true,
        autoResize: true,
        ...config
      };
      
      this.iframe = null;
      this.eventHandlers = new Map();
      this.isReady = false;
      
      this.init();
    }
    
    init() {
      this.createIframe();
      this.setupEventListeners();
      this.injectIframe();
    }
    
    createIframe() {
      this.iframe = document.createElement('iframe');
      
      // Build src URL with config
      const srcUrl = new URL(this.config.src);
      srcUrl.searchParams.set('config', btoa(JSON.stringify(this.config)));
      
      this.iframe.src = srcUrl.toString();
      this.iframe.width = this.config.width;
      this.iframe.height = this.config.height;
      
      // Security settings
      this.iframe.sandbox = 'allow-scripts allow-same-origin allow-forms allow-modals';
      this.iframe.allow = 'microphone; camera; storage-access';
      this.iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      this.iframe.loading = 'lazy';
      
      // Styling
      Object.assign(this.iframe.style, {
        border: 'none',
        borderRadius: '12px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        backgroundColor: '#fff',
        display: 'block',
        width: this.config.width + 'px',
        height: this.config.height + 'px'
      });
      
      this.iframe.className = 'bytewise-chatbot-iframe';
    }
    
    setupEventListeners() {
      window.addEventListener('message', (event) => {
        if (event.source !== this.iframe.contentWindow) return;
        
        const message = event.data;
        if (!message || message.source !== 'bytewise-chatbot') return;
        
        this.handleChatbotMessage(message);
      });
    }
    
    handleChatbotMessage(message) {
      const { type, data } = message;
      
      switch (type) {
        case 'chatbot-ready':
          this.isReady = true;
          this.emit('ready', data);
          console.log('ByteWise Chatbot ready:', data);
          break;
          
        case 'resize-request':
          if (this.config.autoResize) {
            this.resize(data.width, data.height);
          }
          this.emit('resize-request', data);
          break;
          
        case 'message-sent':
          this.emit('message', data);
          console.log('Message sent:', data);
          break;
          
        case 'error':
          this.emit('error', data);
          console.error('Chatbot error:', data);
          break;
          
        case 'analytics':
          this.emit('analytics', data);
          break;
          
        default:
          console.log('Unknown chatbot message:', message);
      }
    }
    
    // Public API methods
    updateConfig(newConfig) {
      this.config = { ...this.config, ...newConfig };
      this.sendMessage('config-update', newConfig);
    }
    
    sendMessage(type, data) {
      if (!this.iframe || !this.iframe.contentWindow) {
        console.warn('Chatbot iframe not ready');
        return;
      }
      
      this.iframe.contentWindow.postMessage({
        type,
        data,
        target: 'bytewise-chatbot',
        source: 'parent-window',
        timestamp: Date.now()
      }, '*');
    }
    
    resize(width, height) {
      if (this.iframe) {
        this.iframe.style.width = width + 'px';
        this.iframe.style.height = height + 'px';
        this.iframe.width = width;
        this.iframe.height = height;
      }
    }
    
    injectMessage(content) {
      this.sendMessage('inject-message', { content, timestamp: Date.now() });
    }
    
    resetConversation() {
      this.sendMessage('reset-conversation', { timestamp: Date.now() });
    }
    
    // Event handling
    on(event, handler) {
      if (!this.eventHandlers.has(event)) {
        this.eventHandlers.set(event, []);
      }
      this.eventHandlers.get(event).push(handler);
    }
    
    off(event, handler) {
      const handlers = this.eventHandlers.get(event) || [];
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
    
    emit(event, data) {
      const handlers = this.eventHandlers.get(event) || [];
      handlers.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Event handler error for ${event}:`, error);
        }
      });
    }
    
    injectIframe() {
      this.container.appendChild(this.iframe);
    }
    
    destroy() {
      if (this.iframe && this.iframe.parentNode) {
        this.iframe.parentNode.removeChild(this.iframe);
      }
      this.eventHandlers.clear();
      this.iframe = null;
    }
  }
  
  // Global API
  window.ByteWiseChatbot = ByteWiseChatbot;
  
  // Auto-initialization for data attributes
  document.addEventListener('DOMContentLoaded', () => {
    const autoElements = document.querySelectorAll('[data-bytewise-chatbot]');
    
    autoElements.forEach(element => {
      const config = {};
      
      // Parse data attributes
      for (const attr of element.attributes) {
        if (attr.name.startsWith('data-chatbot-')) {
          const key = attr.name.replace('data-chatbot-', '').replace(/-([a-z])/g, (g) => g[1].toUpperCase());
          config[key] = attr.value === 'true' ? true : attr.value === 'false' ? false : attr.value;
        }
      }
      
      new ByteWiseChatbot(element, config);
    });
  });
  
})(window);
```

This implementation provides a complete iframe wrapper system with configuration management, event bubbling, and security measures for seamless chatbot embedding! 🚀
