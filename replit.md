# EEGC Essay Tutor

## Overview
An essay revision chatbot system for English for Graduate Communication (EEGC) courses. The system features:
- **Student Mode**: AI-assisted essay revision with Training and Assessment modes
- **Teacher Mode**: Dashboard to view student chat histories and add comments
- **Mock Login**: Role-based authentication (OAuth integration with auth.hkbu.tech pending)
- **AI Integration**: Uses HKBU GenAI platform (students provide their own API keys)

## Tech Stack
### Frontend
- **Framework**: Vue.js 3.5 with Vite 7
- **Styling**: Tailwind CSS 4
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **Port**: 5000

### Backend
- **Framework**: Flask with Flask-SocketIO
- **Database**: PostgreSQL (Replit built-in)
- **AI**: HKBU GenAI platform API
- **Port**: 8000

## Project Structure
```
src/
├── components/
│   ├── dashboard/        # Teacher dashboard components
│   │   └── StudentHistoryModal.vue
│   └── new_EEGC/         # EEGC chatbot components
├── stores/
│   └── auth.js           # Authentication state (Pinia)
├── views/
│   ├── LoginPage.vue     # Mock login with role selection
│   ├── NewEEGC.vue       # Main EEGC essay tutor interface
│   └── TeacherDashboard.vue
└── router/index.js

server/
├── app/routers/
│   ├── chatbot.py        # HKBU GenAI chatbot endpoints
│   ├── database.py       # User/session/message CRUD endpoints
│   └── openrouter.py     # OpenRouter API endpoints
├── migrations/
│   └── 001_init.sql      # Database schema
└── main.py               # Flask app entry point
```

## Database Schema
- **users**: id, username, role (student/teacher), created_at
- **chat_sessions**: id, user_id, title, created_at, updated_at
- **messages**: id, session_id, role, content, created_at
- **teacher_comments**: id, session_id, teacher_id, comment, created_at

## API Endpoints

### Database API (`/api/db/`)
- `POST /users` - Create or get user
- `GET /students` - Get all students (for teachers)
- `POST /sessions` - Create chat session
- `GET /sessions/:user_id` - Get user's sessions
- `POST /messages` - Save message
- `GET /messages/:session_id` - Get session messages
- `POST /comments` - Add teacher comment
- `GET /comments/:session_id` - Get session comments
- `GET /health` - Database health check

### Chatbot API (`/api/chatbot/`)
- `POST /chat` - Send message to HKBU GenAI (requires API key)

## Development
```bash
# Frontend runs on port 5000
npm run dev

# Backend runs on port 8000
cd server && python main.py
```

## User Preferences
- Uses HKBU GenAI platform with user-provided API keys (not Replit AI integration)
- Mock login system (pending OAuth credentials for auth.hkbu.tech)
- Vite dev server proxies /api requests to Flask backend

## Recent Changes (2026-01-05)
- Added PostgreSQL database integration for user/session/message persistence
- Updated auth store with database API integration
- Created teacher dashboard with real-time student data fetching
- Added proper error handling to database routes
- Created SQL migration file for schema reproducibility
