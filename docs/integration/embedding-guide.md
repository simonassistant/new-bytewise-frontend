# 📖 ByteWise AI Chatbot - Embedding Documentation

**Version:** 1.0.0  
**Last Updated:** September 6, 2025  
**Compatibility:** All modern browsers, React, Vue, Angular, WordPress, and vanilla HTML

---

## 🚀 **Quick Start Guide**

### **Method 1: Simple HTML Embedding (Recommended)**

Add this to your HTML page:

```html
<!-- Load the chatbot script -->
<script src="https://chatbot.bytewise.ai/chatbot-embedder.js"></script>

<!-- Add chatbot container with configuration -->
<div data-bytewise-chatbot
     data-chatbot-theme="default"
     data-chatbot-width="400" 
     data-chatbot-height="600"
     data-chatbot-enable-voice="true">
</div>
```

### **Method 2: JavaScript API**

```javascript
// Initialize programmatically
const chatbot = new ByteWiseChatbot('#chatbot-container', {
  theme: 'corporate',
  width: 400,
  height: 600,
  apiProvider: 'hkbu',
  systemPrompt: 'You are a helpful assistant.',
  enableVoice: true,
  enableTyping: true
});

// Listen for events
chatbot.on('ready', () => console.log('Chatbot is ready!'));
chatbot.on('message', (data) => console.log('User sent:', data.content));
```

---

## ⚙️ **Configuration Options**

### **Core Settings**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `src` | string | `https://chatbot.bytewise.ai/embed` | Iframe source URL |
| `width` | number | `400` | Chatbot width in pixels |
| `height` | number | `600` | Chatbot height in pixels |
| `theme` | string | `'default'` | UI theme: `default`, `corporate`, `minimal`, `dark` |
| `apiProvider` | string | `'hkbu'` | AI provider: `hkbu`, `openrouter`, `custom` |
| `autoResize` | boolean | `true` | Enable automatic iframe resizing |

### **AI Configuration**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `systemPrompt` | string | `'You are a helpful AI assistant.'` | AI personality/instructions |
| `welcomeMessage` | string | `'Hello! How can I help you today?'` | First message shown |
| `model` | string | `'gpt-4.1-mini'` | AI model to use |
| `apiKey` | string | `null` | Custom API key (for OpenRouter) |
| `apiEndpoint` | string | `null` | Custom API endpoint |

### **UI Customization**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `primaryColor` | string | `'#6366f1'` | Main theme color (hex) |
| `secondaryColor` | string | `'#8b5cf6'` | Secondary theme color |
| `borderRadius` | string | `'12px'` | Border radius for rounded corners |
| `fontFamily` | string | `'system-ui'` | Font family for text |
| `size` | string | `'normal'` | Size preset: `compact`, `normal`, `expanded` |

### **Feature Flags**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableVoice` | boolean | `true` | Enable voice input |
| `enableTyping` | boolean | `true` | Enable typing input |
| `enableEmail` | boolean | `false` | Enable email integration |
| `contextMemory` | boolean | `true` | Remember conversation context |
| `tokenTracking` | boolean | `true` | Track token usage |
| `exportConversation` | boolean | `true` | Allow conversation export |

### **Security Settings**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `allowedOrigins` | array | `['*']` | Allowed parent page origins |
| `maxMessageLength` | number | `4000` | Maximum message character limit |
| `rateLimitMessages` | number | `60` | Messages per minute limit |

---

## 🎨 **Theme Customization**

### **Built-in Themes**

#### **Default Theme**
```javascript
{
  theme: 'default',
  primaryColor: '#6366f1',
  secondaryColor: '#8b5cf6'
}
```

#### **Corporate Theme**
```javascript
{
  theme: 'corporate',
  primaryColor: '#1f2937',
  secondaryColor: '#374151',
  borderRadius: '8px'
}
```

#### **Minimal Theme**
```javascript
{
  theme: 'minimal',
  primaryColor: '#059669',
  secondaryColor: '#10b981',
  borderRadius: '16px'
}
```

#### **Dark Theme**
```javascript
{
  theme: 'dark',
  primaryColor: '#7c3aed',
  secondaryColor: '#8b5cf6',
  borderRadius: '12px'
}
```

### **Custom Styling**

#### **CSS Custom Properties**
The chatbot exposes CSS custom properties you can override:

```css
.bytewise-chatbot-iframe {
  --primary-color: #your-brand-color;
  --secondary-color: #your-secondary-color;
  --border-radius: 8px;
  --font-family: 'Your Font', sans-serif;
  --shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

#### **Dynamic Theme Updates**
```javascript
// Update theme at runtime
chatbot.updateConfig({
  theme: 'corporate',
  primaryColor: '#your-brand-color',
  secondaryColor: '#your-accent-color'
});
```

---

## 📱 **Responsive Design**

### **Breakpoints**

The chatbot automatically adapts to different screen sizes:

| Screen Size | Width | Height | Features |
|-------------|-------|--------|----------|
| Mobile (< 640px) | 100% | 500px | Touch-optimized, compact UI |
| Tablet (640-1024px) | 400px | 600px | Standard layout |
| Desktop (> 1024px) | 450px | 700px | Full features, larger text |

### **Custom Responsive Behavior**

```javascript
const chatbot = new ByteWiseChatbot('#container', {
  autoResize: true,
  size: window.innerWidth < 768 ? 'compact' : 'normal'
});

// Listen for resize events
window.addEventListener('resize', () => {
  const newSize = window.innerWidth < 768 ? 'compact' : 'normal';
  chatbot.updateConfig({ size: newSize });
});
```

---

## 🔄 **Event System**

### **Available Events**

#### **Lifecycle Events**
- `ready` - Chatbot initialized and ready to use
- `error` - Error occurred (with error details)
- `destroy` - Chatbot was destroyed

#### **User Interaction Events**
- `message` - User sent a message
- `voice-start` - User started voice input
- `voice-end` - User finished voice input
- `typing-start` - User started typing
- `typing-end` - User stopped typing

#### **UI Events**
- `resize-request` - Chatbot requests container resize
- `theme-change` - Theme was updated
- `config-update` - Configuration changed

#### **System Events**
- `token-count` - Token usage updated
- `conversation-export` - Conversation exported
- `email-sent` - Email successfully sent

### **Event Handling Examples**

```javascript
const chatbot = new ByteWiseChatbot('#container', config);

// Basic event handling
chatbot.on('ready', (data) => {
  console.log('Chatbot ready with capabilities:', data.capabilities);
});

chatbot.on('message', (data) => {
  console.log('User message:', data.content);
  console.log('Message timestamp:', data.timestamp);
  
  // Track user engagement
  analytics.track('chatbot_message_sent', {
    length: data.content.length,
    timestamp: data.timestamp
  });
});

chatbot.on('error', (error) => {
  console.error('Chatbot error:', error.message);
  
  // Show user-friendly error message
  showNotification('Chatbot temporarily unavailable', 'error');
  
  // Report error to monitoring service
  errorReporter.captureException(error);
});

// Advanced event handling with context
chatbot.on('resize-request', (data) => {
  if (data.reason === 'content-change') {
    // Smooth resize animation
    animateResize(data.width, data.height);
  }
});

chatbot.on('voice-start', () => {
  // Show listening indicator
  document.getElementById('status').textContent = '🎤 Listening...';
});

chatbot.on('voice-end', () => {
  // Hide listening indicator
  document.getElementById('status').textContent = '';
});
```

---

## 🔧 **API Methods**

### **Configuration Management**

```javascript
// Get current configuration
const config = chatbot.getConfig();

// Update configuration
chatbot.updateConfig({
  theme: 'dark',
  enableVoice: false,
  systemPrompt: 'You are a technical support assistant.'
});

// Reset to defaults
chatbot.resetConfig();

// Export configuration for backup
const configBackup = chatbot.exportConfig();
localStorage.setItem('chatbot-config', configBackup);

// Import saved configuration
const savedConfig = localStorage.getItem('chatbot-config');
chatbot.importConfig(savedConfig);
```

### **Message Management**

```javascript
// Inject a message from parent page
chatbot.injectMessage('Hello from the website!');

// Send system message (appears as bot message)
chatbot.sendSystemMessage('I can help you with your questions.');

// Clear conversation history
chatbot.clearHistory();

// Export conversation
const conversation = chatbot.exportConversation();
downloadAsFile(conversation, 'chat-history.json');
```

### **UI Control**

```javascript
// Manual resize
chatbot.resize(500, 700);

// Hide/show chatbot
chatbot.hide();
chatbot.show();

// Toggle voice input
chatbot.toggleVoice();

// Focus on input
chatbot.focus();

// Set loading state
chatbot.setLoading(true, 'Connecting to AI...');
```

### **Utility Methods**

```javascript
// Check if chatbot is ready
if (chatbot.isReady()) {
  // Safe to interact
}

// Get chatbot status
const status = chatbot.getStatus(); // 'loading', 'ready', 'error'

// Get conversation statistics
const stats = chatbot.getStats();
console.log(`Messages: ${stats.messageCount}, Tokens: ${stats.tokenCount}`);

// Check feature availability
if (chatbot.hasFeature('voice')) {
  // Voice input is supported
}
```

---

## 🔒 **Security Considerations**

### **Content Security Policy (CSP)**

Add these directives to your CSP header:

```http
Content-Security-Policy: 
  frame-src https://chatbot.bytewise.ai;
  connect-src https://chatbot.bytewise.ai https://api.openrouter.ai;
  script-src 'self' https://chatbot.bytewise.ai;
```

### **Iframe Sandboxing**

The chatbot iframe uses these sandbox permissions:

```html
<iframe sandbox="allow-scripts allow-same-origin allow-forms allow-modals allow-storage-access-by-user-activation">
```

### **Origin Validation**

Configure allowed origins for enhanced security:

```javascript
const chatbot = new ByteWiseChatbot('#container', {
  allowedOrigins: [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
    'https://staging.yourdomain.com'
  ]
});
```

### **API Key Security**

**⚠️ Important:** Never expose API keys in client-side code.

```javascript
// ❌ DON'T DO THIS - API key exposed
const chatbot = new ByteWiseChatbot('#container', {
  apiProvider: 'openrouter',
  apiKey: 'sk-or-v1-your-secret-key' // Exposed in browser!
});

// ✅ DO THIS - Use server proxy
const chatbot = new ByteWiseChatbot('#container', {
  apiProvider: 'custom',
  apiEndpoint: '/api/chat' // Your secure backend endpoint
});
```

---

## 🌐 **Framework Integration**

### **React Integration**

#### **Functional Component**
```jsx
import React, { useEffect, useRef, useState } from 'react';

function ChatbotWidget({ config, onMessage }) {
  const containerRef = useRef(null);
  const chatbotRef = useRef(null);
  const [isReady, setIsReady] = useState(false);
  
  useEffect(() => {
    if (containerRef.current && !chatbotRef.current) {
      // Initialize chatbot
      chatbotRef.current = new ByteWiseChatbot(containerRef.current, {
        theme: 'default',
        width: 400,
        height: 600,
        ...config
      });
      
      // Event handlers
      chatbotRef.current.on('ready', () => setIsReady(true));
      chatbotRef.current.on('message', onMessage);
      chatbotRef.current.on('error', (error) => {
        console.error('Chatbot error:', error);
      });
    }
    
    return () => {
      if (chatbotRef.current) {
        chatbotRef.current.destroy();
        chatbotRef.current = null;
      }
    };
  }, []);
  
  // Update config when props change
  useEffect(() => {
    if (chatbotRef.current && isReady) {
      chatbotRef.current.updateConfig(config);
    }
  }, [config, isReady]);
  
  const sendMessage = (message) => {
    if (chatbotRef.current) {
      chatbotRef.current.injectMessage(message);
    }
  };
  
  return (
    <div className="chatbot-container">
      <div ref={containerRef} />
      {!isReady && <div className="loading">Loading chatbot...</div>}
    </div>
  );
}

// Usage
function App() {
  const handleMessage = (message) => {
    console.log('User message:', message);
  };
  
  return (
    <ChatbotWidget 
      config={{ theme: 'corporate', enableVoice: true }}
      onMessage={handleMessage}
    />
  );
}
```

#### **Class Component**
```jsx
import React, { Component } from 'react';

class ChatbotWidget extends Component {
  constructor(props) {
    super(props);
    this.containerRef = React.createRef();
    this.chatbot = null;
    this.state = { isReady: false };
  }
  
  componentDidMount() {
    this.initializeChatbot();
  }
  
  componentDidUpdate(prevProps) {
    if (this.chatbot && prevProps.config !== this.props.config) {
      this.chatbot.updateConfig(this.props.config);
    }
  }
  
  componentWillUnmount() {
    if (this.chatbot) {
      this.chatbot.destroy();
    }
  }
  
  initializeChatbot = () => {
    this.chatbot = new ByteWiseChatbot(this.containerRef.current, {
      theme: 'default',
      ...this.props.config
    });
    
    this.chatbot.on('ready', () => {
      this.setState({ isReady: true });
      if (this.props.onReady) this.props.onReady();
    });
    
    this.chatbot.on('message', this.props.onMessage);
  };
  
  render() {
    return (
      <div className="chatbot-widget">
        <div ref={this.containerRef} />
        {!this.state.isReady && <div>Loading...</div>}
      </div>
    );
  }
}
```

### **Vue 3 Integration**

#### **Composition API**
```vue
<template>
  <div class="chatbot-container">
    <div ref="chatbotContainer" />
    <div v-if="!isReady" class="loading">
      Loading chatbot...
    </div>
    <div v-if="error" class="error">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['ready', 'message', 'error']);

const chatbotContainer = ref(null);
const isReady = ref(false);
const error = ref(null);
let chatbot = null;

onMounted(() => {
  initializeChatbot();
});

onUnmounted(() => {
  if (chatbot) {
    chatbot.destroy();
  }
});

// Watch for config changes
watch(() => props.config, (newConfig) => {
  if (chatbot && isReady.value) {
    chatbot.updateConfig(newConfig);
  }
}, { deep: true });

const initializeChatbot = () => {
  chatbot = new ByteWiseChatbot(chatbotContainer.value, {
    theme: 'default',
    width: 400,
    height: 600,
    ...props.config
  });
  
  chatbot.on('ready', (data) => {
    isReady.value = true;
    error.value = null;
    emit('ready', data);
  });
  
  chatbot.on('message', (message) => {
    emit('message', message);
  });
  
  chatbot.on('error', (err) => {
    error.value = err.message;
    emit('error', err);
  });
};

// Expose methods to parent
defineExpose({
  sendMessage: (message) => {
    if (chatbot) chatbot.injectMessage(message);
  },
  updateConfig: (config) => {
    if (chatbot) chatbot.updateConfig(config);
  },
  isReady: () => isReady.value
});
</script>

<style scoped>
.chatbot-container {
  position: relative;
}

.loading, .error {
  padding: 1rem;
  text-align: center;
  border-radius: 8px;
}

.loading {
  background: #f0f9ff;
  color: #0369a1;
}

.error {
  background: #fef2f2;
  color: #dc2626;
}
</style>
```

#### **Options API**
```vue
<template>
  <div class="chatbot-widget">
    <div ref="chatbotContainer"></div>
  </div>
</template>

<script>
export default {
  name: 'ChatbotWidget',
  props: {
    config: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      chatbot: null,
      isReady: false
    };
  },
  mounted() {
    this.initializeChatbot();
  },
  beforeDestroy() {
    if (this.chatbot) {
      this.chatbot.destroy();
    }
  },
  watch: {
    config: {
      handler(newConfig) {
        if (this.chatbot && this.isReady) {
          this.chatbot.updateConfig(newConfig);
        }
      },
      deep: true
    }
  },
  methods: {
    initializeChatbot() {
      this.chatbot = new ByteWiseChatbot(this.$refs.chatbotContainer, {
        ...this.config
      });
      
      this.chatbot.on('ready', () => {
        this.isReady = true;
        this.$emit('ready');
      });
      
      this.chatbot.on('message', (message) => {
        this.$emit('message', message);
      });
    },
    
    sendMessage(message) {
      if (this.chatbot) {
        this.chatbot.injectMessage(message);
      }
    }
  }
};
</script>
```

### **Angular Integration**

#### **Component**
```typescript
import { 
  Component, 
  ElementRef, 
  Input, 
  Output, 
  EventEmitter, 
  OnInit, 
  OnDestroy, 
  OnChanges,
  SimpleChanges,
  ViewChild 
} from '@angular/core';

declare global {
  interface Window {
    ByteWiseChatbot: any;
  }
}

@Component({
  selector: 'app-chatbot',
  template: `
    <div class="chatbot-container">
      <div #chatbotContainer></div>
      <div *ngIf="!isReady" class="loading">Loading chatbot...</div>
      <div *ngIf="error" class="error">{{ error }}</div>
    </div>
  `,
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit, OnDestroy, OnChanges {
  @ViewChild('chatbotContainer', { static: true }) 
  chatbotContainer!: ElementRef;
  
  @Input() config: any = {};
  @Output() ready = new EventEmitter<any>();
  @Output() message = new EventEmitter<any>();
  @Output() error = new EventEmitter<any>();
  
  private chatbot: any = null;
  isReady = false;
  error: string | null = null;
  
  ngOnInit() {
    this.initializeChatbot();
  }
  
  ngOnDestroy() {
    if (this.chatbot) {
      this.chatbot.destroy();
    }
  }
  
  ngOnChanges(changes: SimpleChanges) {
    if (changes['config'] && this.chatbot && this.isReady) {
      this.chatbot.updateConfig(this.config);
    }
  }
  
  private initializeChatbot() {
    if (!window.ByteWiseChatbot) {
      console.error('ByteWiseChatbot not loaded');
      return;
    }
    
    this.chatbot = new window.ByteWiseChatbot(
      this.chatbotContainer.nativeElement, 
      {
        theme: 'default',
        width: 400,
        height: 600,
        ...this.config
      }
    );
    
    this.chatbot.on('ready', (data: any) => {
      this.isReady = true;
      this.error = null;
      this.ready.emit(data);
    });
    
    this.chatbot.on('message', (message: any) => {
      this.message.emit(message);
    });
    
    this.chatbot.on('error', (err: any) => {
      this.error = err.message;
      this.error.emit(err);
    });
  }
  
  sendMessage(message: string) {
    if (this.chatbot) {
      this.chatbot.injectMessage(message);
    }
  }
  
  updateConfig(config: any) {
    if (this.chatbot) {
      this.chatbot.updateConfig(config);
    }
  }
}
```

#### **Module**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatbotComponent } from './chatbot.component';

@NgModule({
  declarations: [
    ChatbotComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    ChatbotComponent
  ]
})
export class ChatbotModule { }
```

#### **Usage**
```typescript
// app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="app">
      <h1>My Website</h1>
      
      <app-chatbot
        [config]="chatbotConfig"
        (ready)="onChatbotReady($event)"
        (message)="onMessage($event)"
        (error)="onError($event)">
      </app-chatbot>
    </div>
  `
})
export class AppComponent {
  chatbotConfig = {
    theme: 'corporate',
    enableVoice: true,
    systemPrompt: 'You are a helpful customer service assistant.'
  };
  
  onChatbotReady(data: any) {
    console.log('Chatbot ready:', data);
  }
  
  onMessage(message: any) {
    console.log('User message:', message);
  }
  
  onError(error: any) {
    console.error('Chatbot error:', error);
  }
}
```

### **WordPress Integration**

#### **Plugin Structure**
```
bytewise-chatbot/
├── bytewise-chatbot.php
├── includes/
│   ├── class-bytewise-chatbot.php
│   ├── admin.php
│   └── shortcodes.php
├── assets/
│   ├── admin.css
│   └── admin.js
└── readme.txt
```

#### **Main Plugin File**
```php
<?php
/**
 * Plugin Name: ByteWise AI Chatbot
 * Description: Embed ByteWise AI chatbot in your WordPress site
 * Version: 1.0.0
 * Author: ByteWise AI
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class ByteWiseChatbot {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('admin_menu', array($this, 'admin_menu'));
        add_shortcode('bytewise_chatbot', array($this, 'chatbot_shortcode'));
        add_action('wp_footer', array($this, 'add_chatbot_script'));
    }
    
    public function init() {
        // Initialize plugin
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script(
            'bytewise-chatbot',
            'https://chatbot.bytewise.ai/chatbot-embedder.js',
            array(),
            '1.0.0',
            true
        );
    }
    
    public function admin_menu() {
        add_options_page(
            'ByteWise Chatbot Settings',
            'ByteWise Chatbot',
            'manage_options',
            'bytewise-chatbot',
            array($this, 'admin_page')
        );
    }
    
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>ByteWise Chatbot Settings</h1>
            
            <form method="post" action="options.php">
                <?php settings_fields('bytewise_chatbot_settings'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">Theme</th>
                        <td>
                            <select name="bytewise_theme">
                                <option value="default" <?php selected(get_option('bytewise_theme'), 'default'); ?>>Default</option>
                                <option value="corporate" <?php selected(get_option('bytewise_theme'), 'corporate'); ?>>Corporate</option>
                                <option value="minimal" <?php selected(get_option('bytewise_theme'), 'minimal'); ?>>Minimal</option>
                                <option value="dark" <?php selected(get_option('bytewise_theme'), 'dark'); ?>>Dark</option>
                            </select>
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">Width</th>
                        <td>
                            <input type="number" name="bytewise_width" value="<?php echo esc_attr(get_option('bytewise_width', 400)); ?>" min="300" max="800" />
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">Height</th>
                        <td>
                            <input type="number" name="bytewise_height" value="<?php echo esc_attr(get_option('bytewise_height', 600)); ?>" min="400" max="900" />
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">Enable Voice</th>
                        <td>
                            <input type="checkbox" name="bytewise_voice" value="1" <?php checked(1, get_option('bytewise_voice', 1)); ?> />
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">System Prompt</th>
                        <td>
                            <textarea name="bytewise_system_prompt" rows="3" cols="50"><?php echo esc_textarea(get_option('bytewise_system_prompt', 'You are a helpful assistant.')); ?></textarea>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button(); ?>
            </form>
            
            <h2>Usage</h2>
            <p>Use the shortcode <code>[bytewise_chatbot]</code> to display the chatbot in posts or pages.</p>
            <p>You can override settings in the shortcode:</p>
            <code>[bytewise_chatbot theme="dark" width="450" height="650"]</code>
        </div>
        <?php
    }
    
    public function chatbot_shortcode($atts) {
        $atts = shortcode_atts(array(
            'theme' => get_option('bytewise_theme', 'default'),
            'width' => get_option('bytewise_width', 400),
            'height' => get_option('bytewise_height', 600),
            'voice' => get_option('bytewise_voice', 1) ? 'true' : 'false',
            'typing' => 'true',
            'system_prompt' => get_option('bytewise_system_prompt', 'You are a helpful assistant.'),
        ), $atts);
        
        return sprintf(
            '<div data-bytewise-chatbot data-chatbot-theme="%s" data-chatbot-width="%d" data-chatbot-height="%d" data-chatbot-enable-voice="%s" data-chatbot-enable-typing="%s" data-chatbot-system-prompt="%s"></div>',
            esc_attr($atts['theme']),
            intval($atts['width']),
            intval($atts['height']),
            esc_attr($atts['voice']),
            esc_attr($atts['typing']),
            esc_attr($atts['system_prompt'])
        );
    }
    
    public function add_chatbot_script() {
        // Add any additional configuration or initialization
    }
}

// Initialize the plugin
new ByteWiseChatbot();

// Register settings
add_action('admin_init', function() {
    register_setting('bytewise_chatbot_settings', 'bytewise_theme');
    register_setting('bytewise_chatbot_settings', 'bytewise_width');
    register_setting('bytewise_chatbot_settings', 'bytewise_height');
    register_setting('bytewise_chatbot_settings', 'bytewise_voice');
    register_setting('bytewise_chatbot_settings', 'bytewise_system_prompt');
});
?>
```

---

## 🧪 **Testing Integration**

### **Test HTML Page**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Integration Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2rem; }
        .test-section { margin: 2rem 0; padding: 1rem; border: 1px solid #ddd; }
        .chatbot-container { margin: 1rem 0; }
    </style>
</head>
<body>
    <h1>Chatbot Integration Tests</h1>
    
    <!-- Test 1: Basic Integration -->
    <div class="test-section">
        <h2>Test 1: Basic Integration</h2>
        <div data-bytewise-chatbot
             data-chatbot-width="400"
             data-chatbot-height="500">
        </div>
    </div>
    
    <!-- Test 2: Custom Theme -->
    <div class="test-section">
        <h2>Test 2: Custom Theme</h2>
        <div id="custom-chatbot"></div>
        <script>
            const customChatbot = new ByteWiseChatbot('#custom-chatbot', {
                theme: 'corporate',
                width: 450,
                height: 600,
                enableVoice: true
            });
            
            customChatbot.on('ready', () => console.log('Custom chatbot ready'));
        </script>
    </div>
    
    <!-- Test 3: Event Monitoring -->
    <div class="test-section">
        <h2>Test 3: Event Monitoring</h2>
        <div id="monitored-chatbot"></div>
        <div id="event-log" style="margin-top: 1rem; padding: 1rem; background: #f5f5f5; max-height: 200px; overflow-y: auto;"></div>
        
        <script>
            const monitoredChatbot = new ByteWiseChatbot('#monitored-chatbot', {
                theme: 'minimal',
                width: 400,
                height: 550
            });
            
            const eventLog = document.getElementById('event-log');
            
            function logEvent(message) {
                const time = new Date().toLocaleTimeString();
                eventLog.innerHTML += `[${time}] ${message}<br>`;
                eventLog.scrollTop = eventLog.scrollHeight;
            }
            
            monitoredChatbot.on('ready', (data) => {
                logEvent('✅ Chatbot ready: ' + JSON.stringify(data.capabilities));
            });
            
            monitoredChatbot.on('message', (data) => {
                logEvent('💬 Message: ' + data.content);
            });
            
            monitoredChatbot.on('error', (error) => {
                logEvent('❌ Error: ' + error.message);
            });
            
            monitoredChatbot.on('resize-request', (data) => {
                logEvent(`📏 Resize requested: ${data.width}x${data.height}`);
            });
        </script>
    </div>
    
    <script src="https://chatbot.bytewise.ai/chatbot-embedder.js"></script>
</body>
</html>
```

### **Automated Testing Script**
```javascript
// test-integration.js
class ChatbotTester {
    constructor() {
        this.tests = [];
        this.results = [];
    }
    
    addTest(name, testFn) {
        this.tests.push({ name, testFn });
    }
    
    async runTests() {
        console.log('🧪 Starting Chatbot Integration Tests...\n');
        
        for (const test of this.tests) {
            try {
                console.log(`Running: ${test.name}`);
                await test.testFn();
                this.results.push({ name: test.name, status: 'PASS' });
                console.log(`✅ ${test.name} - PASSED\n`);
            } catch (error) {
                this.results.push({ 
                    name: test.name, 
                    status: 'FAIL', 
                    error: error.message 
                });
                console.log(`❌ ${test.name} - FAILED: ${error.message}\n`);
            }
        }
        
        this.printSummary();
    }
    
    printSummary() {
        const passed = this.results.filter(r => r.status === 'PASS').length;
        const failed = this.results.filter(r => r.status === 'FAIL').length;
        
        console.log('📊 Test Summary:');
        console.log(`Total: ${this.results.length}`);
        console.log(`Passed: ${passed}`);
        console.log(`Failed: ${failed}`);
        
        if (failed > 0) {
            console.log('\n❌ Failed Tests:');
            this.results
                .filter(r => r.status === 'FAIL')
                .forEach(r => console.log(`- ${r.name}: ${r.error}`));
        }
    }
}

// Initialize tester
const tester = new ChatbotTester();

// Test 1: Basic Initialization
tester.addTest('Basic Initialization', () => {
    return new Promise((resolve, reject) => {
        const container = document.createElement('div');
        document.body.appendChild(container);
        
        const chatbot = new ByteWiseChatbot(container, {
            src: './iframe-host.html',
            width: 400,
            height: 500
        });
        
        const timeout = setTimeout(() => {
            reject(new Error('Chatbot initialization timeout'));
        }, 10000);
        
        chatbot.on('ready', () => {
            clearTimeout(timeout);
            chatbot.destroy();
            document.body.removeChild(container);
            resolve();
        });
        
        chatbot.on('error', (error) => {
            clearTimeout(timeout);
            reject(error);
        });
    });
});

// Test 2: Configuration Updates
tester.addTest('Configuration Updates', () => {
    return new Promise((resolve, reject) => {
        const container = document.createElement('div');
        document.body.appendChild(container);
        
        const chatbot = new ByteWiseChatbot(container, {
            src: './iframe-host.html',
            theme: 'default'
        });
        
        chatbot.on('ready', () => {
            try {
                // Test config update
                chatbot.updateConfig({ theme: 'dark' });
                
                // Verify config was updated
                const config = chatbot.getConfig();
                if (config.theme !== 'dark') {
                    throw new Error('Configuration update failed');
                }
                
                chatbot.destroy();
                document.body.removeChild(container);
                resolve();
            } catch (error) {
                reject(error);
            }
        });
    });
});

// Test 3: Event Communication
tester.addTest('Event Communication', () => {
    return new Promise((resolve, reject) => {
        const container = document.createElement('div');
        document.body.appendChild(container);
        
        const chatbot = new ByteWiseChatbot(container, {
            src: './iframe-host.html'
        });
        
        let eventsReceived = [];
        
        chatbot.on('ready', () => eventsReceived.push('ready'));
        chatbot.on('message', () => eventsReceived.push('message'));
        
        chatbot.on('ready', () => {
            // Inject test message to trigger message event
            chatbot.injectMessage('Test message');
            
            // Wait for message event
            setTimeout(() => {
                try {
                    if (!eventsReceived.includes('ready')) {
                        throw new Error('Ready event not received');
                    }
                    
                    chatbot.destroy();
                    document.body.removeChild(container);
                    resolve();
                } catch (error) {
                    reject(error);
                }
            }, 2000);
        });
    });
});

// Test 4: Responsive Behavior
tester.addTest('Responsive Behavior', () => {
    return new Promise((resolve, reject) => {
        const container = document.createElement('div');
        document.body.appendChild(container);
        
        const chatbot = new ByteWiseChatbot(container, {
            src: './iframe-host.html',
            width: 400,
            height: 500,
            autoResize: true
        });
        
        chatbot.on('ready', () => {
            let resizeEventReceived = false;
            
            chatbot.on('resize-request', (data) => {
                resizeEventReceived = true;
                
                if (!data.width || !data.height) {
                    reject(new Error('Invalid resize data'));
                    return;
                }
            });
            
            // Trigger resize by updating config
            chatbot.resize(500, 600);
            
            setTimeout(() => {
                try {
                    chatbot.destroy();
                    document.body.removeChild(container);
                    resolve();
                } catch (error) {
                    reject(error);
                }
            }, 1000);
        });
    });
});

// Run tests when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => tester.runTests(), 1000);
    });
} else {
    setTimeout(() => tester.runTests(), 1000);
}
```

---

This comprehensive embedding documentation provides everything needed to integrate the ByteWise chatbot successfully! 🚀
