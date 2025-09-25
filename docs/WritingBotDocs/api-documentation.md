# API Documentation

## Backend Integration

### Base Configuration
- **Production URL**: `https://new-bytewise-backend-production.up.railway.app/api`
- **Development URL**: `http://127.0.0.1:5000/api` (commented out)
- **Configuration File**: `src/components/base_url.js`

## Endpoints

### Chat Endpoint
**URL**: `POST /chatbot/chat`

**Description**: Main endpoint for AI chat interactions

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "chat_history": [
    {
      "role": "system|user|assistant",
      "content": "message content",
      "timestamp": "2025-09-25T10:30:00.000Z"
    }
  ],
  "api_key": "your-hkbu-api-key",
  "model_name": "gpt-5-mini|gpt-5|gpt-4.1-mini|gpt-4.1"
}
```

**Response Format**:
```json
{
  "choices": [
    {
      "message": {
        "content": "AI response content"
      }
    }
  ]
}
```

**Alternative Response Formats**:
```json
{
  "response": "AI response content"
}
```
or
```json
{
  "message": "AI response content"
}
```

## Chat History Structure

### Message Object
```javascript
{
  role: "user" | "assistant" | "system",
  content: "string",
  timestamp: Date
}
```

### Role Types
- **user**: Student input messages
- **assistant**: AI responses
- **system**: Context/instruction messages (not displayed in UI)

## System Message Templates

### Training Mode System Message
```
You are an expert writing assistant designed to help students revise a teacher-provided draft to improve its quality as a point-of-view essay. Your role is to engage in an in-depth conversation with the student, providing clear, constructive feedback based on the provided rubric (Content and Ideas, Organisation and Logical Progression, Vocabulary, Grammar and Sentence Structure). Offer specific suggestions to enhance the draft's relevance, clarity, depth, organisation, vocabulary, and grammar. Ask targeted questions to guide the student in critically evaluating the draft and encourage them to justify their revision choices. Provide appropriate prompts to ensure the conversation remains focused and productive, fostering a robust iterative revision process. Document all exchanges clearly to reflect the depth of the conversation and the student's engagement.

Teacher-provided Draft:
---
[Sample essay content]
```

### Assessment Mode System Message
```
You are an expert writing assistant tasked with helping a student revise their own point-of-view essay draft without any specific prompts. Engage in a detailed, open-ended conversation to guide the student in improving their draft based on the provided rubric (Content and Ideas, Organisation and Logical Progression, Vocabulary, Grammar and Sentence Structure). Offer tailored feedback to enhance the essay's relevance, clarity, depth, logical flow, vocabulary, and grammar. Ask insightful, multi-level questions to encourage critical thinking and help the student evaluate their work. Support an iterative revision process by suggesting specific improvements and encouraging the student to justify their choices. Ensure all exchanges are well-documented, showcasing the depth of the conversation and the student's critical engagement with your suggestions.

Here are the drafts:
Original Draft:
---
[Student's original draft]
---

Final Draft:
---
[Student's revised draft]
---
```

## Available AI Models

1. **gpt-5-mini** (default)
2. **gpt-5**
3. **gpt-4.1-mini**
4. **gpt-4.1**

## Authentication

### HKBU Generative AI Platform
- **API Key Source**: https://genai.hkbu.edu.hk/settings/api-docs
- **Storage**: Browser localStorage as 'chatbot_api_key'
- **Validation**: Connection test with dummy message on setup

### Connection Test
The system validates API connectivity by sending:
```json
{
  "chat_history": [
    {
      "role": "system",
      "content": "connection test, return 1 if you can read the text."
    },
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "api_key": "user-provided-key",
  "model_name": "selected-model"
}
```

## Error Handling

### Client-Side Error Handling
```javascript
try {
  const res = await fetch(`${BASE_URL}/chatbot/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  
  const data = await res.json();
  const reply = data?.choices?.[0]?.message?.content || 
               data?.response || 
               data?.message || "";
               
} catch (error) {
  // Display error message in chat
  chatHistory.value.push({
    role: "assistant",
    content: "⚠️ Error connecting to server.",
    timestamp: new Date()
  });
}
```

### Common Error Scenarios
1. **Network Connection Issues**: Server unreachable
2. **Invalid API Key**: Authentication failure
3. **Model Unavailable**: Selected model not accessible
4. **Rate Limiting**: Too many requests
5. **Invalid Request Format**: Malformed JSON

## Rate Limiting
- No explicit rate limiting documented
- Handled through error responses from backend

## Data Privacy
- API keys stored locally in browser
- Chat history not persisted on server
- Export functionality provides local JSON download

## Development vs Production
- Development: Local Flask server (port 5000)
- Production: Railway-hosted backend
- Configuration managed in `base_url.js`

## Integration Notes
- Backend uses Railway for hosting
- Frontend communicates via HTTPS in production
- CORS configured for cross-origin requests
- JSON-only communication protocol