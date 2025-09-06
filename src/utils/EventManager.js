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
