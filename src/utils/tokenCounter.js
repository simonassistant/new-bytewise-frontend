/**
 * Token Counter Utility
 * Provides approximate token counting for different AI models
 */

/**
 * Approximate token count estimation
 * This is a rough approximation - actual tokenization may vary by model
 * @param {string} text - The text to count tokens for
 * @returns {number} Approximate token count
 */
export function estimateTokens(text) {
  if (!text) return 0;
  
  // Remove extra whitespace
  const cleanText = text.trim().replace(/\s+/g, ' ');
  
  // Rough approximation: 
  // - Average English word is ~1.3 tokens
  // - Punctuation and special chars add tokens
  // - Code and technical terms are often more tokens per word
  
  const words = cleanText.split(' ').length;
  const chars = cleanText.length;
  
  // More conservative estimate for technical/academic content
  return Math.ceil(words * 1.5 + chars * 0.02);
}

/**
 * Get model context limits and information
 * @param {string} modelName - The model identifier
 * @returns {Object} Model information including context limit
 */
export function getModelInfo(modelName) {
  const modelInfo = {
    'google/gemini-flash-1.5': {
      name: 'Google Gemini Flash 1.5',
      contextLimit: 1000000, // 1M tokens
      provider: 'Google',
      inputCost: 0.075, // per 1M tokens
      outputCost: 0.30,  // per 1M tokens
    },
    'anthropic/claude-3-haiku': {
      name: 'Anthropic Claude 3 Haiku',
      contextLimit: 200000, // 200K tokens
      provider: 'Anthropic',
      inputCost: 0.25,
      outputCost: 1.25,
    },
    'openai/gpt-4o-mini': {
      name: 'OpenAI GPT-4o Mini',
      contextLimit: 128000, // 128K tokens
      provider: 'OpenAI',
      inputCost: 0.15,
      outputCost: 0.60,
    },
    default: {
      name: 'Unknown Model',
      contextLimit: 128000, // Conservative default
      provider: 'Unknown',
      inputCost: 0.50,
      outputCost: 2.00,
    }
  };
  
  return modelInfo[modelName] || modelInfo.default;
}

/**
 * Calculate context window usage for a conversation
 * @param {Array} messages - Array of conversation messages
 * @param {string} modelName - The model identifier
 * @returns {Object} Usage information
 */
export function calculateContextUsage(messages, modelName = 'google/gemini-flash-1.5') {
  const modelInfo = getModelInfo(modelName);
  
  // Calculate total tokens used in conversation
  let totalTokens = 0;
  let inputTokens = 0;
  let outputTokens = 0;
  
  messages.forEach(message => {
    const tokens = estimateTokens(message.content || '');
    totalTokens += tokens;
    
    if (message.role === 'user') {
      inputTokens += tokens;
    } else if (message.role === 'assistant') {
      outputTokens += tokens;
    }
  });
  
  // Add system prompt tokens (approximate)
  const systemPromptTokens = 150; // Rough estimate
  totalTokens += systemPromptTokens;
  
  const usage = {
    totalTokens,
    inputTokens,
    outputTokens,
    systemTokens: systemPromptTokens,
    contextLimit: modelInfo.contextLimit,
    usagePercentage: Math.round((totalTokens / modelInfo.contextLimit) * 100),
    remainingTokens: modelInfo.contextLimit - totalTokens,
    modelInfo
  };
  
  return usage;
}

/**
 * Format number with appropriate units (K, M)
 * @param {number} num - The number to format
 * @returns {string} Formatted number string
 */
export function formatTokenCount(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  } else {
    return num.toString();
  }
}

/**
 * Get usage color based on percentage
 * @param {number} percentage - Usage percentage (0-100)
 * @returns {string} Color class or hex color
 */
export function getUsageColor(percentage) {
  if (percentage < 50) return '#10b981'; // Green
  if (percentage < 75) return '#f59e0b'; // Yellow
  if (percentage < 90) return '#f97316'; // Orange
  return '#ef4444'; // Red
}
