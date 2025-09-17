# Technical Specification: Three-Bot Testing System

## System Overview

The Three-Bot Testing System automates the testing and evaluation of the Bytewise Frontend training mode using three interconnected AI bots that simulate realistic student-teacher interactions.

## Architecture Diagram

```
┌─────────────────┐    API Call    ┌─────────────────┐    Response    ┌─────────────────┐
│   Student Bot   │──────────────▶│   Trainer Bot   │──────────────▶│   Student Bot   │
│  (OpenRouter)   │                │   (Existing)    │                │  (OpenRouter)   │
└─────────────────┘                └─────────────────┘                └─────────────────┘
        │                                   │                                   │
        │                          Chat History Logs                           │
        │                                   │                                   │
        └─────────────────────────────────▶ │ ◀─────────────────────────────────┘
                                            ▼
                                   ┌─────────────────┐
                                   │  Reviewer Bot   │
                                   │  (OpenRouter)   │
                                   └─────────────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Analysis Report │
                                   └─────────────────┘
```

## Component Specifications

### 1. Student Bot (OpenRouter API)

#### Purpose
Simulate realistic student interactions with various skill levels and learning objectives.

#### Technical Details
- **API**: OpenRouter API
- **Model**: GPT-4 or Claude (configurable)
- **Input Schema**:
  ```json
  {
    "persona": "beginner|intermediate|advanced",
    "focus_area": "content|structure|vocabulary|grammar",
    "conversation_context": [...],
    "platform_info": {...}
  }
  ```

#### Student Personas
1. **Beginner Student**
   - Limited vocabulary usage
   - Basic grammar questions
   - Needs explicit guidance
   - Simple follow-up questions

2. **Intermediate Student**
   - Moderate writing skills
   - Asks for clarification on complex concepts
   - Can engage in deeper discussions
   - Shows some critical thinking

3. **Advanced Student**
   - Strong foundation but seeking refinement
   - Challenges AI suggestions
   - Asks sophisticated questions
   - Demonstrates critical evaluation skills

#### Response Patterns
- Natural language with appropriate skill level
- Contextual follow-up questions
- Realistic confusion and clarification requests
- Engagement with feedback received

### 2. Trainer Bot (Existing System)

#### Current Implementation
- **Endpoint**: `POST https://new-bytewise-backend-production.up.railway.app/api/chatbot/chat_openrouter`
- **Input**: `{ chat_history: [...] }`
- **Output**: `{ choices: [{ message: { content: string } }] }`

#### Integration Points
- Chat history management
- Session state tracking
- Mode switching (training/assessment)
- Progress metrics calculation

### 3. Reviewer Bot (OpenRouter API)

#### Purpose
Analyze conversation logs and provide improvement recommendations.

#### Analysis Capabilities
1. **Conversation Quality Metrics**
   - Depth of engagement
   - Follow-up question frequency
   - Critical thinking demonstration
   - Iterative improvement cycles

2. **Learning Effectiveness**
   - Skill development progression
   - Feedback utilization
   - Knowledge retention indicators
   - Engagement patterns

3. **Platform Improvement Areas**
   - UI/UX optimization suggestions
   - Content gap identification
   - Feature enhancement recommendations
   - Student guidance improvements

#### Output Formats
- JSON structured reports
- Markdown summaries
- CSV data for analysis
- Visual charts (future enhancement)

## Implementation Architecture

### File Structure
```
src/
├── testing-system/
│   ├── bots/
│   │   ├── StudentBot.js
│   │   ├── ReviewerBot.js
│   │   └── BotOrchestrator.js
│   ├── api/
│   │   ├── OpenRouterClient.js
│   │   ├── TrainerAPIClient.js
│   │   └── ChatHistoryManager.js
│   ├── config/
│   │   ├── personas.json
│   │   ├── scenarios.json
│   │   └── settings.js
│   └── utils/
│       ├── ConversationAnalyzer.js
│       ├── ReportGenerator.js
│       └── Logger.js
```

### API Communication Flow

#### 1. Student Bot → Trainer Bot
```javascript
// Student bot generates message
const studentMessage = await generateStudentResponse(context, persona);

// Send to trainer bot
const response = await fetch(`${BASE_URL}/chatbot/chat_openrouter`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chat_history: [
      ...previousHistory,
      { role: 'user', content: studentMessage, timestamp: new Date() }
    ]
  })
});

const trainerResponse = await response.json();
```

#### 2. Conversation Loop Management
```javascript
class ConversationOrchestrator {
  async runScenario(scenario, maxExchanges = 10) {
    let exchangeCount = 0;
    
    while (exchangeCount < maxExchanges) {
      // Student generates response
      const studentMsg = await this.studentBot.generateResponse();
      
      // Send to trainer
      const trainerResponse = await this.trainerAPI.sendMessage(studentMsg);
      
      // Log interaction
      this.logger.logExchange(studentMsg, trainerResponse);
      
      // Check termination conditions
      if (this.shouldTerminate(trainerResponse)) break;
      
      exchangeCount++;
    }
    
    // Generate analysis
    return await this.reviewerBot.analyzeConversation(this.logger.getHistory());
  }
}
```

### Data Models

#### Chat Message
```typescript
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    persona?: string;
    confidence?: number;
    analysis?: object;
  };
}
```

#### Test Scenario
```typescript
interface TestScenario {
  id: string;
  name: string;
  description: string;
  persona: 'beginner' | 'intermediate' | 'advanced';
  focusArea: 'content' | 'structure' | 'vocabulary' | 'grammar';
  initialPrompt: string;
  expectedOutcomes: string[];
  maxExchanges: number;
}
```

#### Analysis Report
```typescript
interface AnalysisReport {
  sessionId: string;
  timestamp: Date;
  scenario: TestScenario;
  metrics: {
    totalExchanges: number;
    followUpQuestions: number;
    revisionCycles: number;
    engagementScore: number;
  };
  insights: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  conversationLog: ChatMessage[];
}
```

## Security and Privacy

### API Key Management
- Environment variables for OpenRouter keys
- Secure storage and rotation
- Rate limiting implementation
- Error handling for API failures

### Data Privacy
- No persistent storage of sensitive data
- Anonymized conversation logs
- GDPR compliance considerations
- Data retention policies

## Configuration Management

### Environment Variables
```bash
OPENROUTER_API_KEY=your_api_key_here
TRAINER_API_BASE_URL=https://new-bytewise-backend-production.up.railway.app/api
LOG_LEVEL=info
MAX_CONVERSATION_LENGTH=20
ANALYSIS_MODEL=gpt-4
STUDENT_MODEL=gpt-3.5-turbo
```

### Feature Flags
- Enable/disable testing system
- Model selection per bot type
- Logging verbosity levels
- Report generation formats

## Testing and Validation

### Unit Tests
- Individual bot response generation
- API client functionality
- Data model validation
- Utility function testing

### Integration Tests
- End-to-end conversation flows
- API communication reliability
- Error handling scenarios
- Performance benchmarks

### Quality Assurance
- Manual review of generated conversations
- Validation against expected outcomes
- Performance monitoring
- Resource usage tracking

## User Interface Requirements (Phase 5)

### Testing Dashboard GUI

#### Purpose
Provide transparency and visibility into the automated testing system for administrators and stakeholders.

#### Key Features
1. **Real-time Status Display**
   - Active bot conversations indicator
   - Current testing scenarios running
   - System health and API status
   - Queue of pending tests

2. **Testing Metrics Dashboard**
   - Success/failure rates
   - Response time analytics
   - Conversation quality scores
   - Historical trend charts

3. **Control Panel**
   - Start/stop testing scenarios
   - Configure bot personas and parameters
   - Schedule automated test runs
   - Emergency stop functionality

4. **Reporting Interface**
   - Generated analysis reports
   - Downloadable conversation logs
   - Improvement recommendations
   - Export functionality (PDF, CSV, JSON)

#### Technical Implementation
```javascript
// Vue component structure
src/views/TestingDashboard.vue
├── components/
│   ├── StatusIndicator.vue
│   ├── MetricsChart.vue
│   ├── ControlPanel.vue
│   ├── ConversationViewer.vue
│   └── ReportGenerator.vue
```

#### User Permissions
- **Administrator**: Full access to all features
- **Monitor**: Read-only access to status and reports
- **Public**: Basic transparency indicators

#### Transparency Features
- Public status page showing testing is active
- Anonymized conversation examples
- System improvement announcements
- User notification when testing affects their experience

## Deployment Strategy

### Development Phase
1. Local testing environment
2. Mock API responses for development
3. Unit test coverage
4. Code review process

### Integration Phase
1. Staging environment testing
2. Limited production testing
3. Performance optimization
4. Documentation completion

### Production Deployment
1. Feature flag enabled rollout
2. Monitoring and alerting
3. Gradual usage increase
4. Feedback collection and iteration

---

*Document Version: 1.0*
*Last Updated: September 17, 2025*
*Author: Simon Wang*
*Reviewer: [Pending - Kaitai Zhang]*
