# 📖 ByteWise AI Chatbot - Integration Documentation

Welcome to the ByteWise AI Chatbot integration documentation! This comprehensive guide will help you embed the chatbot in your website or application.

## 🚀 Quick Start

### Simple HTML Integration
```html
<script src="https://chatbot.bytewise.ai/chatbot-embedder.js"></script>
<div data-bytewise-chatbot data-chatbot-theme="default"></div>
```

### JavaScript API
```javascript
const chatbot = new ByteWiseChatbot('#container', {
  theme: 'corporate',
  enableVoice: true
});
```

## 📚 Documentation Overview

### 📖 [Embedding Guide](./embedding-guide.md)
Complete integration guide covering:
- Configuration options and validation
- Event system and communication
- Theme customization
- Framework integrations (React, Vue, Angular, WordPress)
- Security considerations

### 🛠️ [Troubleshooting Guide](./troubleshooting-guide.md)
Comprehensive troubleshooting resources:
- Common issues and solutions
- Browser compatibility
- Performance optimization
- Debug tools and error reporting

### 🎮 [Interactive Examples](../public/embedding-examples.html)
Live demonstration page with:
- Multiple embedding methods
- Real-time configuration controls
- Event logging and monitoring
- Framework-specific examples

## 🔧 Key Features

- ✅ **iFrame Embedding** - Secure, isolated chatbot integration
- ✅ **PostMessage Communication** - Bidirectional event system
- ✅ **Responsive Design** - Mobile-first, auto-resizing
- ✅ **Theme Customization** - Multiple built-in themes + custom CSS
- ✅ **Voice Input** - Browser-native speech recognition
- ✅ **Configuration Management** - Reactive config with validation
- ✅ **Security** - CSP headers, origin validation, sandboxing

## 📋 Integration Checklist

- [ ] Review [Embedding Guide](./embedding-guide.md) for your framework
- [ ] Test with [Interactive Examples](../public/embedding-examples.html)
- [ ] Configure CSP headers for your domain
- [ ] Set up error monitoring and logging
- [ ] Test across target browsers and devices
- [ ] Review [Troubleshooting Guide](./troubleshooting-guide.md) for common issues

## 🆘 Need Help?

- **Documentation Issues**: Check [Troubleshooting Guide](./troubleshooting-guide.md)
- **Integration Problems**: Review [Embedding Guide](./embedding-guide.md) examples
- **Custom Requirements**: Contact support@bytewise.ai

## 📊 Performance Benchmarks

- **Load Time**: <3 seconds initial load
- **Memory Usage**: <50MB for typical usage
- **API Response**: <2 seconds for OpenRouter integration
- **Compatibility**: Chrome 60+, Firefox 55+, Safari 11+, Edge 79+

---

**Ready to integrate?** Start with the [Embedding Guide](./embedding-guide.md) or explore the [Interactive Examples](../public/embedding-examples.html)! 🚀
