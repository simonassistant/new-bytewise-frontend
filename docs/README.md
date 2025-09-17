# Bytewise Frontend Documentation

## Project Overview

The Bytewise Frontend is a Vue 3-based web application that provides multiple AI-powered chatbot interfaces for educational and writing assistance purposes.

### Live Instances
- **Writing Bot**: https://textbot.hkbu.tech/writingBot
- **Main Chat Interface**: http://chat.hkbu.tech

### Technology Stack
- **Frontend**: Vue 3 + Vite
- **Styling**: Tailwind CSS
- **State Management**: Pinia
- **Router**: Vue Router 4
- **Real-time Communication**: Socket.IO
- **Additional Features**: PDF generation, Markdown rendering with KaTeX

## Project Structure

```
src/
├── botConfig/          # Chatbot configuration files
├── components/         # Reusable Vue components
├── views/             # Page components
├── router/            # Vue Router configuration
└── assets/            # Static assets
```

## Available Chatbots

The application includes various specialized chatbot configurations:
- Writing assistance (IELTS, academic writing)
- Course-specific tutors (GCAP3187, GCAP3247, EEGC)
- Policy discourse analysis
- Discussion preparation
- Paraphrasing assistance

## Development Status

- ✅ Writing chatbot completed and tested
- ✅ Multiple bot configurations implemented
- 🔄 Active development by Kaitai Zhang (@Bob8259)

## Documentation Goals

This documentation aims to:
1. Provide clear user guidance for the chatbot interfaces
2. Document the system architecture for future developers
3. Coordinate development efforts without interfering with active work
4. Create a foundation for comprehensive documentation as the project evolves

---

*Last updated: September 17, 2025*
*Developer: Kaitai Zhang (@Bob8259)*
