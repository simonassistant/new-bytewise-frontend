# Poe Models Chat GUI

A modern web-based interface for chatting with different Poe AI models and saving chat history.

## Features

- 🤖 **Multiple AI Models**: Chat with GPT-3.5, Claude, Gemini, and other Poe models
- 💬 **Real-time Chat**: Interactive chat interface with typing indicators
- 📚 **Chat History**: Automatically save and load previous conversations
- 🎨 **Modern UI**: Beautiful, responsive design that works on desktop and mobile
- ⚡ **Fast & Efficient**: Optimized for quick responses and smooth interactions
- 🔒 **Local Storage**: Chat history stored locally in your browser

## Available Models

The interface includes these representative models:

### Text Models
- **GPT-3.5 Turbo** (11 points) - General-purpose, good performance
- **Claude Haiku 3** (17 points) - Fast, affordable Anthropic model
- **Gemini 2.0 Flash** (9 points) - Google's fast, low-cost model
- **GPT-4o** (224 points) - High-quality OpenAI model
- **Claude Sonnet 3.5** (276 points) - Advanced Anthropic model
- **Mistral Medium** (218 points) - Strong mid-range model
- **F1 Preview** (1 point) - Ultra-low cost for testing

## Setup Instructions

### 1. Install Dependencies

```bash
cd /Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/AItutorDev/poe_local
pip install -r requirements_gui.txt
```

### 2. Verify API Key

Make sure your Poe API key is properly configured in:
```
/Users/simonwang/Documents/Usage/ObSync/Vault4sync/AItutorDoc/poe/poeKey.md
```

### 3. Start the Server

```bash
python poe_gui_server.py
```

### 4. Open the Interface

Open your web browser and go to:
```
http://localhost:5000
```

## Usage Guide

### Starting a Chat

1. **Select a Model**: Choose from the dropdown in the left sidebar
2. **Type Your Message**: Use the text input at the bottom
3. **Send**: Press Enter or click the send button (➤)

### Managing Chat History

- **View History**: Click on any conversation in the left sidebar
- **Load Previous Chat**: Click on a history item to continue that conversation
- **Clear History**: Use the "Clear All" button to remove all saved chats

### Model Selection

Each model has different characteristics:

- **Cost-Effective**: F1 Preview (1 point), Gemini 2.0 Flash (9 points)
- **Balanced**: GPT-3.5 Turbo (11 points), Claude Haiku 3 (17 points)
- **High-Quality**: GPT-4o (224 points), Claude Sonnet 3.5 (276 points)

### Tips for Best Results

1. **Start Simple**: Use F1 Preview or Gemini 2.0 Flash for basic questions
2. **Complex Tasks**: Switch to GPT-4o or Claude Sonnet for detailed analysis
3. **Save Important Chats**: The interface automatically saves your conversations
4. **Experiment**: Try different models for the same question to see variations

## API Endpoints

The server provides these endpoints:

- `GET /` - Main GUI interface
- `POST /api/chat` - Send message to AI model
- `GET /api/models` - Get available models
- `GET /api/balance` - Check account balance
- `GET /api/health` - Server health check

## File Structure

```
poe_local/
├── poe_gui.html              # Main GUI interface
├── poe_gui_server.py         # Flask backend server
├── poe_client.py             # Poe API client
├── poe_models_info.py       # Model information
├── config.py                 # Configuration
├── requirements_gui.txt      # GUI dependencies
└── chatHistory/             # Chat history storage (auto-created)
```

## Troubleshooting

### Common Issues

1. **"Poe API client not initialized"**
   - Check that your API key file exists and contains a valid key
   - Verify the path in `config.py` is correct

2. **"Error sending message"**
   - Check your internet connection
   - Verify you have sufficient Poe points
   - Try a different model

3. **Server won't start**
   - Make sure port 5000 is available
   - Check that all dependencies are installed
   - Try running with `python3` instead of `python`

### Getting Help

- Check the server console for error messages
- Verify your Poe API key is working with the basic client
- Try the health check endpoint: `http://localhost:5000/api/health`

## Advanced Usage

### Custom Model Selection

You can modify the available models by editing the `modelInfo` object in `poe_gui.html`:

```javascript
const modelInfo = {
    'Your-Custom-Model': {
        name: 'Your Custom Model',
        description: 'Description of your model',
        points: 100
    }
    // ... other models
};
```

### Chat History Management

Chat history is stored in your browser's localStorage. To backup or transfer:

1. Open browser developer tools (F12)
2. Go to Application/Storage tab
3. Find "poeChatHistory" in localStorage
4. Copy the JSON data

## Security Notes

- Chat history is stored locally in your browser
- API keys are handled server-side only
- No data is sent to external servers except Poe API
- All communication uses HTTPS when available

## Performance Tips

- Use lower-cost models for simple questions
- Clear old chat history periodically
- Close unused browser tabs to free memory
- Use the health check endpoint to monitor server status

---

**Happy Chatting! 🤖💬**
