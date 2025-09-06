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
