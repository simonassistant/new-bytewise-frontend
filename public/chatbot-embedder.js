// Parent website embedder script
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
