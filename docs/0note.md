- we need to develop the chatbot that can be embedded in iFrame
- the chatbot should be customised with system prompt
- the chatbot should be able to remember the context
- we need a version that uses the API key of open router
- we need to implement the mail service
- there are two repos

  - https://github.com/Bob8259/new-bytewise-frontend
  - https://github.com/tesolchina/new-bytewise-frontend

  we need to pull

  - https://github.com/Bob8259/new-bytewise-frontend and compare with
  - 
  - https://github.com/tesolchina/new-bytewise-frontend and identify some codes that are useful especially the chat module

please do not write any codes yet; let's write a step by step plan like a checklist below

===============

plan and checklist (6 Sept 2025)

## 🎯 Project Requirements Analysis

- ✅ Embeddable chatbot via iFrame
- ✅ Customizable system prompt
- ✅ Context memory retention
- ✅ OpenRouter API key integration
- ✅ Mail service implementation
- ✅ Repository synchronization and code comparison

## 📋 Step-by-Step Development Plan

### Phase 1: Repository Analysis & Code Audit (Week 1)

- [X] **1.1** Clone and analyze Bob8259/new-bytewise-frontend repository

  - [X] Examine current chat module implementation ✅ **REST+WebSocket dual architecture identified**
  - [X] Document existing API integrations ✅ **HKBU API system with token management**  
  - [X] Identify reusable components ✅ **7 bot configs, context engine, Pinia store**
  - [X] Check current context management system ✅ **Advanced multi-state conversation tracking**

📊 **Analysis Report Created**: `docs/analysis/bob-repo-analysis.md`
- [x] **1.2** Compare with tesolchina/new-bytewise-frontend repository

  - [x] Identify differences in chat functionality ✅ **Your UI excellence vs Bob's logic excellence**
  - [x] Extract useful chat module components ✅ **ChatBubble, InputModeToggle, AvatarPanel + Bob's context engine**
  - [x] Document Sprint 1 WeChat-style improvements ✅ **WeChat bubbles, hybrid input, animations documented**
  - [x] Assess hybrid voice+typing system compatibility ✅ **95% compatible, clear integration strategy**

📊 **Comparison Report Created**: `docs/analysis/repository-comparison.md`
- [x] **1.3** Create comprehensive code comparison report

  - [x] Feature matrix comparison table ✅ **Complete feature-by-feature analysis with scores**
  - [x] Identify best practices from both repos ✅ **Context management, token tracking, UI patterns documented**
  - [x] List components to merge/migrate ✅ **Migration matrix with priorities and effort estimates**
  - [x] Document technical debt and improvements needed ✅ **Critical issues and performance improvements identified**

📊 **Comprehensive Report Created**: `docs/analysis/comprehensive-comparison-report.md`

---

## ✅ **Phase 1 Complete Summary:**
- **Bob's Analysis**: Production logic, context management, token system
- **Repository Comparison**: Your UI excellence vs Bob's backend robustness  
- **Integration Strategy**: Merge Bob's foundation + Your modern components
- **Technical Roadmap**: 3-week integration plan with clear priorities

### Phase 2: iFrame Embeddable Architecture (Week 2)

- [x] **2.1** Design iFrame-compatible architecture

  - [x] Create standalone chatbot component ✅ **EmbeddableChatbot.vue root + ChatbotCore.vue designed**
  - [x] Implement postMessage communication system ✅ **Bidirectional protocol with security validation**
  - [x] Design responsive iframe sizing mechanism ✅ **Auto-resize with content-aware calculations**
  - [x] Plan cross-origin security considerations ✅ **CSP policies, origin validation, secure API handling**

📐 **Architecture Document Created**: `docs/design/iframe-architecture.md`
- [x] **2.2** Develop iframe wrapper and parent communication ✅ **Complete implementation with HTML template, config management, and event system**

  - [x] Create iframe host HTML template ✅ **iframe-host.html with security headers and error handling**
  - [x] Implement configuration passing mechanism ✅ **ConfigurationManager.js with validation and reactive updates**
  - [x] Design event bubbling system (messages, resize, etc.) ✅ **EventManager.js with postMessage protocol**
  - [x] Add iframe sandbox security settings ✅ **Production-ready security policies and chatbot-embedder.js**

🖼️ **Implementation Files Created**: `public/iframe-host.html`, `src/utils/ConfigurationManager.js`, `src/utils/EventManager.js`, `public/chatbot-embedder.js`
- [x] **2.3** Create embedding documentation and examples ✅ **Complete comprehensive documentation suite**

  - [x] Write iframe integration guide ✅ **embedding-guide.md with full API reference and examples**
  - [x] Create sample HTML embedding examples ✅ **embedding-examples.html with interactive demos**
  - [x] Document configuration options ✅ **Complete configuration reference with validation**
  - [x] Add troubleshooting guide for common issues ✅ **troubleshooting-guide.md with solutions and debugging tools**

📚 **Documentation Suite Created**: `docs/integration/embedding-guide.md`, `docs/integration/troubleshooting-guide.md`, `public/embedding-examples.html`

---

## ✅ **Phase 2 Complete Summary:**
- **iFrame Architecture**: Complete standalone chatbot with postMessage communication
- **Security Implementation**: Production-ready CSP policies, origin validation, sandboxing
- **Configuration System**: Reactive configuration management with validation
- **Event System**: Bidirectional communication with parent window
- **Documentation**: Comprehensive integration guides and troubleshooting resources
- **Examples**: Interactive demos and framework-specific integration guides

### Phase 3: System Prompt Customization (Week 2-3)

- [ ] **3.1** Design flexible prompt system

  - [ ] Create prompt template management
  - [ ] Implement dynamic prompt injection
  - [ ] Design persona/role-based prompts
  - [ ] Add prompt validation and sanitization
- [ ] **3.2** Build prompt customization interface

  - [ ] Create prompt editor component
  - [ ] Add real-time prompt preview
  - [ ] Implement prompt library/presets
  - [ ] Add import/export functionality for prompts
- [ ] **3.3** Integrate with existing bot configurations

  - [ ] Merge with current botConfig system
  - [ ] Preserve existing IELTS, GCAP analyst configurations
  - [ ] Ensure backward compatibility
  - [ ] Add migration path for existing configurations

### Phase 4: Context Memory Enhancement (Week 3-4)

- [x] **4.1** Analyze current context retention system ✅ **Complete comprehensive analysis with memory limitations, bottlenecks, and improvement plan**

  - [x] Audit existing WebSocket chat history ✅ **Documented dual REST/WebSocket architecture with persistence gaps**
  - [x] Identify memory limitations and bottlenecks ✅ **Found token ignorance, simple FIFO pruning, no summarization**
  - [x] Document current session management ✅ **Mapped localStorage strategy, session lifecycle, and recovery issues**
  - [x] Plan improved persistence strategy ✅ **Designed sliding window, summarization, and token-aware management**

📊 **Analysis Report Created**: `docs/analysis/context-retention-analysis.md`
- [ ] **4.2** Implement enhanced context management

  - [ ] Design sliding window context system
  - [ ] Add conversation summarization for long chats
  - [ ] Implement local storage context backup
  - [ ] Create context export/import functionality
- [ ] **4.3** Add context analytics and optimization

  - [ ] Implement token counting for context management
  - [ ] Add context relevance scoring
  - [ ] Create context pruning algorithms
  - [ ] Add memory usage monitoring dashboard

---

## ✅ **Phase 4.1 Complete Summary:**
- **Context Analysis**: Comprehensive audit of current memory management systems
- **Memory Limitations**: Identified token ignorance, simple FIFO pruning, no summarization
- **Session Management**: Documented localStorage strategy and recovery gaps
- **Improvement Plan**: Designed sliding window, summarization, and token-aware management
- **Technical Roadmap**: 4-phase enhancement plan with performance targets

### Phase 5: OpenRouter API Integration (Week 4-5)

- [ ] **5.1** Research OpenRouter API specifications

  - [ ] Document OpenRouter API endpoints
  - [ ] Compare with current API integration
  - [ ] Plan API key management system
  - [ ] Design fallback mechanism for API failures
- [ ] **5.2** Implement OpenRouter API adapter

  - [ ] Create OpenRouter API client
  - [ ] Add API key validation and testing
  - [ ] Implement streaming response handling
  - [ ] Add error handling and retry logic
- [ ] **5.3** Create API configuration interface

  - [ ] Design API provider selection UI
  - [ ] Add API key input and validation
  - [ ] Create API performance monitoring
  - [ ] Implement usage tracking and quotas

### Phase 6: Mail Service Implementation (Week 5-6)

- [ ] **6.1** Design mail service architecture

  - [ ] Choose email service provider (SendGrid, AWS SES, etc.)
  - [ ] Design email template system
  - [ ] Plan conversation export to email
  - [ ] Create email scheduling system
- [ ] **6.2** Implement email functionality

  - [ ] Create email sending service
  - [ ] Design conversation summary emails
  - [ ] Add email subscription management
  - [ ] Implement email analytics and tracking
- [ ] **6.3** Integrate with chatbot interface

  - [ ] Add "Email Conversation" button
  - [ ] Create email settings panel
  - [ ] Implement automated email reports
  - [ ] Add email notification preferences

### Phase 7: Integration & Testing (Week 6-7)

- [ ] **7.1** Merge best features from both repositories

  - [ ] Integrate Sprint 1 WeChat-style UI improvements
  - [ ] Port hybrid voice+typing system to embeddable version
  - [ ] Merge avatar panel system (if applicable to iframe)
  - [ ] Ensure clean separation of concerns
- [ ] **7.2** End-to-end testing

  - [ ] Test iframe embedding in various websites
  - [ ] Verify cross-browser compatibility
  - [ ] Test context retention across sessions
  - [ ] Validate email service functionality
  - [ ] Performance testing with OpenRouter API
- [ ] **7.3** Documentation and deployment

  - [ ] Create comprehensive user documentation
  - [ ] Write developer integration guide
  - [ ] Prepare deployment scripts
  - [ ] Create demo website with embedded chatbot

### Phase 8: Optimization & Production Ready (Week 7-8)

- [ ] **8.1** Performance optimization

  - [ ] Minimize bundle size for iframe loading
  - [ ] Implement lazy loading for components
  - [ ] Optimize API calls and caching
  - [ ] Add progressive web app features
- [ ] **8.2** Security hardening

  - [ ] Implement CSP headers for iframe
  - [ ] Add input sanitization and validation
  - [ ] Secure API key storage and transmission
  - [ ] Add rate limiting and abuse prevention
- [ ] **8.3** Production deployment

  - [ ] Set up CI/CD pipeline
  - [ ] Configure monitoring and logging
  - [ ] Deploy to production environment
  - [ ] Create rollback procedures

## 🔧 Technical Stack Decisions

- [ ] **Frontend**: Vue 3 + Composition API (maintain current)
- [ ] **Build**: Vite (current) with iframe-specific build config
- [ ] **API**: OpenRouter integration + existing WebSocket
- [ ] **Email**: Service provider TBD (SendGrid recommended)
- [ ] **Storage**: LocalStorage + optional backend persistence
- [ ] **Deployment**: Railway (current) + CDN for iframe assets

## 📊 Success Metrics

- [ ] iFrame loads in <3 seconds
- [ ] Context retention >95% accuracy
- [ ] Email delivery success rate >98%
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive iframe functionality
- [ ] OpenRouter API integration with <2s response time

## 🚨 Risk Mitigation

- [ ] Backup plan for OpenRouter API downtime
- [ ] Cross-origin iframe security review
- [ ] Context memory overflow handling
- [ ] Email service provider backup options
- [ ] Repository merge conflict resolution strategy
