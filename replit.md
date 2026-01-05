# Bytewise Frontend-Only Application

## Overview
This is a frontend-only Vue.js application for an educational chatbot platform. It provides text-based chatbot and voice avatar functionality using direct API calls to OpenRouter and Azure Speech Services.

## Architecture
- **Frontend Only**: No backend server required
- **Direct API Calls**: Uses OpenRouter API directly from the frontend for chat completions
- **Azure Speech**: Uses Azure Speech SDK with subscription key for text-to-speech and speech-to-text
- **Supabase**: Optional database integration for storing comments and feedback

## Key Features
1. **Text Chatbot** (`/chat/:botId`) - Interactive text-based chat with AI
2. **Voice Avatar** (`/avatar/:avatarId`) - Voice-enabled AI avatar with speech synthesis

## Environment Variables Required
Set these in Replit Secrets:

- `VITE_OPENROUTER_API_KEY` - OpenRouter API key for chat completions
- `VITE_SUPABASE_URL` - (Optional) Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - (Optional) Supabase anonymous key

## User-Provided Keys (stored in browser localStorage)
For security, some API keys are provided by users through the UI rather than environment variables:

- **Azure Speech Key** - Users enter their Azure Speech subscription key in the Avatar page settings
- **HKBU API Key** - Users enter their HKBU GenAI API key in the Chat page settings

## Project Structure
```
src/
├── lib/
│   ├── chatApi.js      # Direct API calls to OpenRouter and HKBU
│   └── supabase.js     # Supabase client for database operations
├── views/
│   ├── HomePage.vue    # Landing page
│   ├── ChatPage.vue    # Text chatbot interface
│   └── AvatarPage.vue  # Voice avatar interface
├── components/
│   ├── text_chatbot/   # Chat UI components
│   └── avatar/         # Avatar UI and speech components
└── router/
    └── index.js        # Vue Router configuration
```

## Running the Application
The application runs on port 5000 using Vite dev server.

## Recent Changes (2026-01-05)
- Removed backend server - all API calls now direct from frontend
- Removed all EEGC essay editing features
- Updated to use OpenRouter direct API calls instead of backend proxy
- Updated Azure Speech to use subscription key instead of token endpoint
- Changed email functionality to use mailto: links instead of backend email service
- Added Supabase client for optional database integration

## API Providers Supported
1. **OpenRouter** - Default provider, uses environment variable for API key
2. **HKBU GenAI** - Alternative provider, requires user-provided API key in UI

## User Preferences
- Keep the application frontend-only for simplicity
- Use environment variables for sensitive API keys
- Support both text and voice interaction modes
