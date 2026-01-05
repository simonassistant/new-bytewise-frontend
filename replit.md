# Bytewise Learning Platform

## Overview
A Vue.js learning platform with AI-powered chatbots and voice avatars. Features a marketplace for discovering learning apps and a unified chat interface supporting both text and voice interaction modes.

## Architecture
- **Frontend**: Vue.js SPA with Vite, Tailwind CSS
- **Backend (BFF)**: Flask server handling OAuth and AI compute proxy
- **Authentication**: OAuth 2.0 via auth.hkbu.tech platform
- **AI Compute**: Provided by the main platform (no user API keys needed)

## Key Features
1. **Learning Marketplace** (`/`) - Browse and search AI learning assistants
2. **Unified Chat** (`/chat/:appId`) - Combined text and voice interface
   - Toggle between typing and speaking
   - Optional avatar display
   - Session reports and history

## Project Structure
```
src/
├── lib/
│   ├── chatApi.js      # API calls (will use backend proxy when OAuth configured)
│   └── supabase.js     # Optional database client
├── views/
│   ├── HomePage.vue    # Marketplace with search
│   └── ChatWorkspace.vue # Unified chat interface
├── components/
│   ├── text_chatbot/   # Chat store and components
│   └── avatar/         # Avatar display and speech
├── botConfig/          # JSON configs for each learning app
└── router/
    └── index.js        # Vue Router

server/
└── main.py             # Flask backend for OAuth and AI proxy
```

## Environment Variables

### Required for Production
- `OAUTH_CLIENT_ID` - OAuth client ID from platform
- `OAUTH_CLIENT_SECRET` - OAuth client secret from platform
- `OAUTH_REDIRECT_URI` - Callback URL (e.g., https://yourapp.com/api/auth/callback)
- `SESSION_SECRET` - Random secret for Flask sessions
- `FRONTEND_ORIGIN` - Frontend URL for CORS

### Development (Temporary)
- `VITE_OPENROUTER_API_KEY` - For testing without platform OAuth

### Optional
- `VITE_SUPABASE_URL` - Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Supabase anonymous key

## OAuth Integration (Pending)

Once you receive the OAuth credentials from the platform admin:

1. Set the environment variables:
   - `OAUTH_CLIENT_ID`
   - `OAUTH_CLIENT_SECRET`
   - `OAUTH_REDIRECT_URI`

2. Update `src/lib/chatApi.js` to call the backend proxy instead of OpenRouter directly

3. The platform will provide:
   - User authentication
   - AI compute (no user API keys)
   - User database access

## Running the Application

- **Frontend**: Port 5000 (Vite dev server)
- **Backend**: Port 3000 (Flask)

## Recent Changes (2026-01-05)
- Created unified ChatWorkspace combining text and voice modes
- Built marketplace homepage showing ALL apps without pagination
- Added category-based dropdown menus in header (Career, GCAP, IELTS, TCM, Other)
- Added lightweight backend for OAuth integration
- Removed separate ChatPage/AvatarPage in favor of unified interface
- Fixed text/voice mode toggle with graceful handling when Azure credentials unavailable

## User Flow
1. User visits marketplace → browses or searches apps
2. Clicks "Start Chat" → enters unified chat workspace
3. Can toggle between text (type) and voice (speak) modes
4. Avatar display is optional and can be toggled

## Bot Configuration
Each learning app is defined in `src/botConfig/*.json` with:
- `name`: Display name
- `systemPrompt`: AI instructions
- `welcomePrompt`: Initial greeting
- `model`: AI model to use
- `gender`: Avatar gender (male/female)
- `appearance`: Avatar appearance
- `reportGenerationInstructions`: For session reports
