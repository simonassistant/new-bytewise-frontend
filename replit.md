# ByteWise Frontend

## Overview
A Vue.js 3 frontend application for ByteWise, featuring chatbot interfaces, avatar components, and educational/writing bot tools.

## Tech Stack
- **Framework**: Vue.js 3.5
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **State Management**: Pinia
- **Routing**: Vue Router 4

## Project Structure
```
src/
├── assets/           # Static assets
├── botConfig/        # Bot configuration JSON files
├── components/       # Vue components
│   ├── avatar/       # Avatar/video chat components
│   ├── new_EEGC/     # EEGC educational components
│   ├── text_chatbot/ # Text chatbot components
│   └── writing_bot/  # Writing assistance components
├── router/           # Vue Router configuration
├── views/            # Page-level components
├── App.vue           # Root component
├── main.js           # Application entry point
└── style.css         # Global styles
```

## Development
- **Port**: 5000 (configured in vite.config.js)
- **Command**: `npm run dev`

## Deployment
- **Type**: Static site
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
