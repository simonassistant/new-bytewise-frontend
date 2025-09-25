# WritingBot Component Analysis

## Component Overview

The `WritingBot.vue` component is the main interface for the AI-powered writing assistant. It provides three distinct modes for different types of writing assistance.

## Component Structure

### Template Structure
- Header with title and description
- Mode selection buttons (Briefing, Training, Assessment)
- Main content area that changes based on mode
- Chat interface (for Training and Assessment modes)
- API configuration section (for Briefing mode)

### Key Data Properties

```javascript
const currentMode = ref("briefing");  // Current active mode
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });  // Progress tracking
const originalDraft = ref("");  // Student's original draft (Assessment mode)
const finalDraft = ref("");     // Student's revised draft (Assessment mode)
const chatHistory = ref([]);    // Chat conversation history
const isConnected = ref(false); // API connection status
const apiKey = ref("");         // HKBU API key
const model = ref("gpt-5-mini"); // Selected AI model
```

## Mode Functionality

### 1. Briefing Mode
- **Purpose**: Display assessment rubrics and guidelines
- **Features**: 
  - Task 1: Point-of-View Essay with Guided Chatbot Revision (10%)
  - Task 2: AI-Assisted Review of Student Draft (10%)
  - Detailed rubric tables with 5-point scales
  - API configuration interface

### 2. Training Mode
- **Purpose**: Guided essay revision with teacher-provided sample
- **Features**:
  - Skills dashboard showing development areas
  - Progress tracking
  - Interactive chat with AI assistant
  - Sample essay provided for practice
  - Export chat history functionality

### 3. Assessment Mode
- **Purpose**: Independent essay revision of student's own work
- **Features**:
  - Original draft input area
  - Final draft comparison
  - Progress tracking with detailed metrics
  - Three-column layout (skills, chat, drafts)

## API Integration

### Backend Endpoint
- Base URL: `https://new-bytewise-backend-production.up.railway.app/api`
- Endpoint: `/chatbot/chat`
- Method: POST

### Request Format
```javascript
{
  chat_history: [...],  // Array of message objects
  api_key: "...",      // HKBU API key
  model_name: "..."    // Selected model (gpt-5-mini, gpt-5, etc.)
}
```

## Key Methods

### Mode Management
- `switchMode(mode)`: Changes between modes and initializes appropriate state
- Updates greeting messages and resets statistics

### Chat Functionality
- `sendMessage()`: Handles user input and API communication
- `scrollToBottom()`: Auto-scrolls chat to latest message
- `renderMarkdown()`: Processes AI responses with markdown formatting

### API Management
- `connectAPI()`: Tests connection and validates API key
- `clearAPI()`: Resets API configuration
- `showNotification()`: Displays connection status messages

### Assessment Features
- `confirmDraft()`: Locks original draft and copies to final draft
- `confirmFinalDraft()`: Generates comparison report
- `exportChatHistory()`: Downloads chat log as JSON

## Styling and UI

### CSS Framework
- **Tailwind CSS**: Primary styling framework
- **Responsive Design**: Mobile-first approach with md: and lg: breakpoints
- **Color Scheme**: Indigo primary, gray neutrals, status colors (green, red, purple)

### Key UI Components
- **Skill Badges**: Color-coded development areas
- **Session Stats**: Progress indicators with colored badges
- **Chat Messages**: Differentiated user/AI styling with timestamps
- **Rubric Tables**: Structured assessment criteria display

## Dependencies

### Core Vue 3
- `ref`, `computed`, `nextTick`, `onMounted`
- Composition API throughout

### External Libraries
- `markdown-it`: Markdown processing for AI responses
- Axios integration through base_url configuration

## Performance Considerations

### State Management
- Reactive refs for real-time updates
- Computed properties for derived state
- Local storage for API key persistence

### Chat Optimization
- Separate payload history from display history
- System message injection for context
- Efficient scroll management

## Security Features

### API Key Handling
- Password-type input field
- Local storage persistence
- Connection validation before use

### Content Safety
- HTML disabled in markdown rendering
- Input sanitization through markdown-it
- Controlled message format

## Future Enhancement Areas

1. **Advanced Analytics**: More detailed progress metrics
2. **Template System**: Pre-defined conversation starters
3. **Multi-language Support**: International student support
4. **Offline Mode**: Basic functionality without API
5. **Export Options**: PDF, Word document generation
6. **Collaboration Features**: Peer review integration

## Deployment Notes

- Deployed at: https://textbot.hkbu.tech/writingBot
- Route: `/writingBot` in Vue Router
- Production build via Vite
- Railway backend integration