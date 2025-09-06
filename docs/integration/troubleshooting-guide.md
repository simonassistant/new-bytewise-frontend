# ⚠️ ByteWise AI Chatbot - Troubleshooting Guide

**Last Updated:** September 6, 2025  
**Version:** 1.0.0

---

## 🚨 **Common Issues & Solutions**

### **1. Chatbot Not Loading**

#### **Symptoms:**
- Empty container or loading spinner stuck
- Console error: `ByteWiseChatbot is not defined`
- Iframe not appearing

#### **Solutions:**

**Check Script Loading:**
```javascript
// Verify script is loaded
if (typeof ByteWiseChatbot === 'undefined') {
    console.error('ByteWiseChatbot script not loaded');
    // Load script dynamically
    const script = document.createElement('script');
    script.src = 'https://chatbot.bytewise.ai/chatbot-embedder.js';
    script.onload = () => {
        // Initialize chatbot after script loads
        initializeChatbot();
    };
    document.head.appendChild(script);
}
```

**Container Issues:**
```javascript
// Ensure container exists
const container = document.getElementById('chatbot-container');
if (!container) {
    console.error('Chatbot container not found');
    return;
}

// Check container visibility
const styles = window.getComputedStyle(container);
if (styles.display === 'none' || styles.visibility === 'hidden') {
    console.warn('Chatbot container is hidden');
}
```

**Network Issues:**
```javascript
// Test connectivity
fetch('https://chatbot.bytewise.ai/health')
    .then(response => {
        if (!response.ok) {
            throw new Error('Service unavailable');
        }
        console.log('Chatbot service is available');
    })
    .catch(error => {
        console.error('Cannot reach chatbot service:', error);
        // Show fallback UI
        showFallbackChat();
    });
```

---

### **2. Configuration Not Applied**

#### **Symptoms:**
- Default theme/settings despite custom configuration
- Configuration updates not reflected
- Data attributes ignored

#### **Solutions:**

**Verify Configuration Syntax:**
```javascript
// ❌ Wrong
const chatbot = new ByteWiseChatbot('#container', {
    theme: 'corporate',  // Missing comma can break entire config
    width: 400
    height: 600  // Syntax error
});

// ✅ Correct
const chatbot = new ByteWiseChatbot('#container', {
    theme: 'corporate',
    width: 400,
    height: 600
});
```

**Check Data Attributes:**
```html
<!-- ❌ Wrong attribute names -->
<div data-bytewise-chatbot
     data-theme="corporate"
     data-width="400">
</div>

<!-- ✅ Correct with prefix -->
<div data-bytewise-chatbot
     data-chatbot-theme="corporate"
     data-chatbot-width="400">
</div>
```

**Configuration Validation:**
```javascript
const config = {
    theme: 'corporate',
    width: 400,
    height: 600
};

// Validate before initializing
function validateConfig(config) {
    const validThemes = ['default', 'corporate', 'minimal', 'dark'];
    
    if (config.theme && !validThemes.includes(config.theme)) {
        console.warn(`Invalid theme: ${config.theme}. Using default.`);
        config.theme = 'default';
    }
    
    if (config.width && (config.width < 300 || config.width > 800)) {
        console.warn(`Invalid width: ${config.width}. Using default.`);
        config.width = 400;
    }
    
    return config;
}

const chatbot = new ByteWiseChatbot('#container', validateConfig(config));
```

---

### **3. Iframe Security Errors**

#### **Symptoms:**
- Console errors about blocked frames
- `X-Frame-Options` or CSP violations
- Cross-origin communication failures

#### **Solutions:**

**CSP Configuration:**
```http
# Add to your server headers
Content-Security-Policy: 
    frame-src https://chatbot.bytewise.ai;
    script-src 'self' https://chatbot.bytewise.ai;
    connect-src https://chatbot.bytewise.ai https://api.openrouter.ai;
```

**Origin Validation:**
```javascript
// Configure allowed origins
const chatbot = new ByteWiseChatbot('#container', {
    allowedOrigins: [
        'https://yourdomain.com',
        'https://www.yourdomain.com'
    ]
});
```

**HTTPS Requirements:**
```javascript
// Check if page is served over HTTPS
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
    console.warn('Chatbot requires HTTPS in production');
    // Show warning to user
    showSecurityWarning();
}
```

**Development CORS Issues:**
```javascript
// For local development only
const chatbot = new ByteWiseChatbot('#container', {
    src: window.location.protocol === 'https:' 
        ? 'https://chatbot.bytewise.ai/embed'
        : 'http://localhost:3000/embed',  // Dev server
    allowedOrigins: ['*']  // Only for development!
});
```

---

### **4. Event Communication Problems**

#### **Symptoms:**
- Events not firing
- `postMessage` errors in console
- Parent-child communication failing

#### **Solutions:**

**Event Handler Debugging:**
```javascript
const chatbot = new ByteWiseChatbot('#container', {});

// Add debug logging
chatbot.on('ready', (data) => {
    console.log('✅ Chatbot ready:', data);
});

chatbot.on('error', (error) => {
    console.error('❌ Chatbot error:', error);
    // Check specific error types
    if (error.message.includes('postMessage')) {
        console.log('PostMessage communication failed - checking origins');
    }
});

// Monitor all postMessage events
window.addEventListener('message', (event) => {
    console.log('📨 Received message:', event.origin, event.data);
});
```

**Timing Issues:**
```javascript
// Wait for DOM and scripts to load
document.addEventListener('DOMContentLoaded', () => {
    // Add additional delay if needed
    setTimeout(() => {
        initializeChatbot();
    }, 100);
});

// Or use intersection observer for lazy loading
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            initializeChatbot();
            observer.unobserve(entry.target);
        }
    });
});

observer.observe(document.getElementById('chatbot-container'));
```

**Message Validation:**
```javascript
// Add message validation
window.addEventListener('message', (event) => {
    // Validate origin
    if (!event.origin.includes('chatbot.bytewise.ai')) {
        console.warn('Message from untrusted origin:', event.origin);
        return;
    }
    
    // Validate message structure
    if (!event.data || !event.data.type) {
        console.warn('Invalid message format:', event.data);
        return;
    }
    
    console.log('Valid message received:', event.data);
});
```

---

### **5. Responsive Layout Issues**

#### **Symptoms:**
- Chatbot doesn't resize on mobile
- Layout breaks on small screens
- Iframe overflow or clipping

#### **Solutions:**

**Responsive Container Setup:**
```css
.chatbot-container {
    width: 100%;
    max-width: 400px;
    height: 600px;
    max-height: 80vh;
    margin: 0 auto;
    position: relative;
}

@media (max-width: 768px) {
    .chatbot-container {
        width: 100%;
        max-width: none;
        height: 500px;
        max-height: 70vh;
    }
}
```

**Dynamic Sizing:**
```javascript
function getResponsiveConfig() {
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 1024;
    
    return {
        width: isMobile ? window.innerWidth - 40 : isTablet ? 380 : 400,
        height: isMobile ? Math.min(500, window.innerHeight * 0.7) : 600,
        size: isMobile ? 'compact' : 'normal',
        autoResize: true
    };
}

const chatbot = new ByteWiseChatbot('#container', getResponsiveConfig());

// Update on resize
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        chatbot.updateConfig(getResponsiveConfig());
    }, 250);
});
```

**Viewport Issues:**
```javascript
// Check viewport meta tag
const viewportMeta = document.querySelector('meta[name="viewport"]');
if (!viewportMeta) {
    console.warn('Missing viewport meta tag for mobile responsiveness');
    
    // Add viewport meta tag
    const meta = document.createElement('meta');
    meta.name = 'viewport';
    meta.content = 'width=device-width, initial-scale=1.0';
    document.head.appendChild(meta);
}
```

---

### **6. Voice Input Not Working**

#### **Symptoms:**
- Microphone icon disabled or missing
- No audio permissions prompt
- Voice input starts but doesn't process

#### **Solutions:**

**Check Browser Support:**
```javascript
function checkVoiceSupport() {
    if (!navigator.mediaDevices) {
        console.warn('MediaDevices API not supported');
        return false;
    }
    
    if (!navigator.mediaDevices.getUserMedia) {
        console.warn('getUserMedia not supported');
        return false;
    }
    
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn('Speech Recognition API not supported');
        return false;
    }
    
    return true;
}

if (!checkVoiceSupport()) {
    // Initialize chatbot without voice
    const chatbot = new ByteWiseChatbot('#container', {
        enableVoice: false
    });
}
```

**HTTPS Requirement:**
```javascript
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
    console.error('Voice input requires HTTPS');
    showHTTPSWarning();
}
```

**Permission Handling:**
```javascript
async function requestMicrophonePermission() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop()); // Clean up
        console.log('Microphone permission granted');
        return true;
    } catch (error) {
        console.error('Microphone permission denied:', error);
        showMicrophonePermissionError();
        return false;
    }
}

// Pre-request permission before initializing chatbot
requestMicrophonePermission().then(hasPermission => {
    const chatbot = new ByteWiseChatbot('#container', {
        enableVoice: hasPermission
    });
});
```

---

### **7. Performance Issues**

#### **Symptoms:**
- Slow chatbot loading
- High memory usage
- Laggy interactions

#### **Solutions:**

**Lazy Loading:**
```javascript
// Load chatbot only when needed
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            loadChatbot();
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

function loadChatbot() {
    const script = document.createElement('script');
    script.src = 'https://chatbot.bytewise.ai/chatbot-embedder.js';
    script.onload = initializeChatbot;
    document.head.appendChild(script);
}
```

**Memory Management:**
```javascript
// Proper cleanup
let chatbot = null;

function initializeChatbot() {
    // Destroy existing instance
    if (chatbot) {
        chatbot.destroy();
        chatbot = null;
    }
    
    chatbot = new ByteWiseChatbot('#container', config);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (chatbot) {
        chatbot.destroy();
    }
});
```

**Resource Optimization:**
```javascript
// Preload critical resources
const preloadLink = document.createElement('link');
preloadLink.rel = 'preload';
preloadLink.href = 'https://chatbot.bytewise.ai/chatbot-embedder.js';
preloadLink.as = 'script';
document.head.appendChild(preloadLink);

// Use requestIdleCallback for non-critical initialization
if ('requestIdleCallback' in window) {
    requestIdleCallback(initializeChatbot);
} else {
    setTimeout(initializeChatbot, 100);
}
```

---

## 🔍 **Debugging Tools**

### **Debug Mode**

Enable debug mode for detailed logging:

```javascript
const chatbot = new ByteWiseChatbot('#container', {
    debug: true,  // Enable debug logging
    
    // Add event listeners for debugging
    onReady: (data) => console.log('Debug - Ready:', data),
    onMessage: (msg) => console.log('Debug - Message:', msg),
    onError: (err) => console.error('Debug - Error:', err)
});

// Global debug helper
window.debugChatbot = chatbot;
```

### **Network Debugging**

Monitor network requests:

```javascript
// Override fetch to log requests
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    console.log('Fetch request:', url, options);
    
    return originalFetch(url, options)
        .then(response => {
            console.log('Fetch response:', url, response.status);
            return response;
        })
        .catch(error => {
            console.error('Fetch error:', url, error);
            throw error;
        });
};
```

### **Browser Console Commands**

Useful console commands for debugging:

```javascript
// Check chatbot status
window.debugChatbot?.getStatus()

// Get configuration
window.debugChatbot?.getConfig()

// Test message sending
window.debugChatbot?.injectMessage('Test message')

// Check event listeners
window.debugChatbot?.eventHandlers

// Force resize
window.debugChatbot?.resize(500, 700)
```

---

## 📊 **Browser Compatibility**

### **Supported Browsers**

| Browser | Version | Voice | Typing | Notes |
|---------|---------|-------|--------|-------|
| Chrome | 60+ | ✅ | ✅ | Full support |
| Firefox | 55+ | ⚠️ | ✅ | Limited voice support |
| Safari | 11+ | ❌ | ✅ | No voice input |
| Edge | 79+ | ✅ | ✅ | Full support |
| iOS Safari | 11+ | ❌ | ✅ | No voice input |
| Android Chrome | 60+ | ✅ | ✅ | Full support |

### **Feature Detection**

```javascript
function detectFeatures() {
    const features = {
        postMessage: 'postMessage' in window,
        localStorage: 'localStorage' in window,
        fetch: 'fetch' in window,
        webGL: hasWebGLSupport(),
        voice: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window,
        mediaDevices: 'mediaDevices' in navigator,
        intersectionObserver: 'IntersectionObserver' in window
    };
    
    console.log('Browser features:', features);
    return features;
}

function hasWebGLSupport() {
    try {
        const canvas = document.createElement('canvas');
        return !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
    } catch(e) {
        return false;
    }
}
```

---

## 🆘 **Support Resources**

### **Error Reporting**

```javascript
// Automatic error reporting
chatbot.on('error', (error) => {
    // Send to your error tracking service
    if (window.Sentry) {
        Sentry.captureException(error);
    }
    
    // Or send to your own endpoint
    fetch('/api/chatbot-error', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            error: error.message,
            stack: error.stack,
            userAgent: navigator.userAgent,
            url: window.location.href,
            timestamp: new Date().toISOString()
        })
    });
});
```

### **Health Check Endpoint**

Test service availability:

```javascript
async function healthCheck() {
    try {
        const response = await fetch('https://chatbot.bytewise.ai/health', {
            method: 'GET',
            timeout: 5000
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Service health:', data);
            return true;
        }
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}
```

### **Contact Support**

If issues persist after trying these solutions:

1. **GitHub Issues**: [https://github.com/bytewise-ai/chatbot/issues](https://github.com/bytewise-ai/chatbot/issues)
2. **Email**: support@bytewise.ai
3. **Documentation**: [https://docs.bytewise.ai](https://docs.bytewise.ai)

Include the following information:
- Browser and version
- Console error messages
- Configuration used
- Steps to reproduce
- Expected vs actual behavior

---

This troubleshooting guide covers the most common issues and their solutions! 🛠️
