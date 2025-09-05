# ByteWise Frontend Documentation

**Project**: ByteWise AI Chatbot Frontend  
**Repository**: `tesolchina/new-bytewise-frontend` (forked from `Bob8259/new-bytewise-frontend`)  
**Last Updated**: September 5, 2025

---

## 📁 Documentation Structure

### 🎯 Sprint Planning & Management
- [`docs/sprints/SPRINT_MANAGEMENT_GUIDE.md`](sprints/SPRINT_MANAGEMENT_GUIDE.md) - Complete sprint methodology
- [`docs/sprints/SPRINT_TEMPLATE.md`](sprints/SPRINT_TEMPLATE.md) - Template for creating new sprints
- [`docs/sprints/sprint-01-foundation-deployment.md`](sprints/sprint-01-foundation-deployment.md) - First sprint (completed)

### 🚀 Deployment Documentation
- [`docs/deployment/RAILWAY_DEPLOYMENT.md`](deployment/RAILWAY_DEPLOYMENT.md) - Complete Railway deployment guide
- [`docs/deployment/QUICK_START_RAILWAY.md`](deployment/QUICK_START_RAILWAY.md) - Quick deployment reference
- [`docs/deployment/NOTE_FOR_BOB.md`](deployment/NOTE_FOR_BOB.md) - Summary of deployment fixes

### 🛠️ Development & Collaboration
- [`docs/collaboration/DEVELOPMENT_WORKFLOW.md`](collaboration/DEVELOPMENT_WORKFLOW.md) - Fork-based workflow guide
- [`docs/collaboration/DEVELOPMENT_LOG_TEMPLATE.md`](collaboration/DEVELOPMENT_LOG_TEMPLATE.md) - Daily log template
- [`docs/development/email-feature-integration-guide.md`](development/email-feature-integration-guide.md) - Email functionality
- [`docs/development/integration-plan-email-module.md`](development/integration-plan-email-module.md) - Email module planning

### 📊 Technical Documentation
- [`docs/memory-optimization-plan.md`](memory-optimization-plan.md) - Performance optimization strategies
- [`docs/token-counter-development-log.md`](token-counter-development-log.md) - Token counter implementation
- [`docs/token-counter-impact-analysis.md`](token-counter-impact-analysis.md) - Token counter impact analysis

### 🔧 Configuration Management
- [`config/README.md`](../config/README.md) - Configuration file organization
- [`config/deployment/`](../config/deployment/) - Railway deployment configurations
- [`config/serve.json`](../config/serve.json) - Static file serving configuration

### � Development Logs
- [`logs/development-log-2025-09-05.md`](../logs/development-log-2025-09-05.md) - Sprint 1 foundation work
- [`logs/debug.log`](../logs/debug.log) - Bob's previous debugging and fixes

### 🧪 Test Results
- [`test-results/`](../test-results/) - Testing reports and validation results

---

## 🎯 Quick Navigation

### For New Developers:
1. Start with [`RAILWAY_DEPLOYMENT.md`](deployment/RAILWAY_DEPLOYMENT.md) for deployment setup
2. Review development logs in [`logs/`](../logs/) for context
3. Check test results for feature validation

### For Deployment:
1. Follow [`QUICK_START_RAILWAY.md`](deployment/QUICK_START_RAILWAY.md)
2. Set environment variables as specified
3. Configure custom domain for https://avatartutor.hkbu.tech/

### For Feature Development:
1. Review existing development documentation
2. Check memory optimization guidelines
3. Follow the established patterns from logs

---

## 🏗️ Project Architecture

### Core Features:
- **Multi-Bot Chat System**: Text-based AI conversations
- **Avatar Mode**: Voice-enabled chat with microphone input
- **Report Generation**: PDF/Markdown export with email functionality
- **Token Tracking**: Real-time usage monitoring
- **Memory Optimization**: Efficient conversation handling

### Technical Stack:
- **Frontend**: Vue 3 + Vite + Pinia + Vue Router
- **Styling**: Tailwind CSS v4
- **Audio**: MediaRecorder API + WebSocket streaming
- **Build**: Vite with optimized code splitting
- **Deployment**: Railway with Node.js 20.19.0

---

*Documentation organized and maintained by development team*  
*For questions or updates, refer to development logs or create issues*
