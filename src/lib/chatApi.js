const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || ''

export async function testAIConnection() {
  const apiKey = import.meta.env.VITE_OPENROUTER_API_KEY
  
  if (!apiKey) {
    return { 
      connected: false, 
      error: 'API key not configured',
      provider: 'openrouter'
    }
  }

  try {
    const response = await fetch(OPENROUTER_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'openai/gpt-4.1-mini',
        messages: [{ role: 'user', content: 'Hi' }],
        max_tokens: 5,
      }),
    })

    if (response.ok) {
      return { connected: true, provider: 'openrouter' }
    } else {
      const errorText = await response.text()
      return { connected: false, error: `API error: ${response.status}`, provider: 'openrouter' }
    }
  } catch (e) {
    return { connected: false, error: e.message, provider: 'openrouter' }
  }
}

export async function chatWithOpenRouter(chatHistory, modelName = 'openai/gpt-4.1-mini', temperature = 0.5) {
  const apiKey = import.meta.env.VITE_OPENROUTER_API_KEY
  
  if (!apiKey) {
    console.error('OPENROUTER_API_KEY not configured')
    return { error: 'OPENROUTER_API_KEY not configured' }
  }

  const response = await fetch(OPENROUTER_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: modelName,
      messages: chatHistory,
      stream: false,
      temperature,
    }),
  })

  if (!response.ok) {
    const errorText = await response.text()
    return { error: `OpenRouter API error: ${response.status} - ${errorText}` }
  }

  return response.json()
}

export async function chatWithHKBU(chatHistory, apiKey, modelName = 'gpt-4', topP = 1.0) {
  const apiVersion = '2024-12-01-preview'
  const url = `https://genai.hkbu.edu.hk/api/v0/rest/deployments/${modelName}/chat/completions?api-version=${apiVersion}`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messages: chatHistory,
      top_p: topP,
      stream: false,
    }),
  })

  if (!response.ok) {
    const errorText = await response.text()
    return { error: `HKBU API error: ${response.status} - ${errorText}` }
  }

  return response.json()
}

export function preprocessChatHistory(chatHistory) {
  const processed = []
  let firstAssistantRemoved = false

  for (const msg of chatHistory) {
    const role = msg.role
    let content = msg.content

    if (!content) continue

    if (Array.isArray(content)) {
      content = content.map(c => typeof c === 'object' ? c.text || '' : String(c)).join(' ')
    } else {
      content = String(content)
    }

    if (role === 'system') {
      processed.push({ role: 'system', content })
    } else if (role === 'assistant') {
      if (!firstAssistantRemoved) {
        firstAssistantRemoved = true
        continue
      }
      processed.push({ role: 'system', content })
    } else if (role === 'user') {
      processed.push({ role: 'user', content })
    }
  }

  return processed
}
