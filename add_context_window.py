#!/usr/bin/env python3
"""
Add Context Window Indicator to Chat.vue
This script adds context window tracking functionality to the Vue chatbot.
"""

import re

def add_context_window_functions(content):
    """Add context window calculation functions after formatNumber function"""
    
    # Find the end of formatNumber function
    format_number_pattern = r'(function formatNumber\(num\) \{[^}]*\})'
    
    context_functions = '''

// Context Window Calculation Functions
function getCurrentContextLimit() {
  const currentModel = isOpenRouterMode.value ? "google/gemini-flash-1.5" : "default";
  return CONTEXT_LIMITS[currentModel] || CONTEXT_LIMITS.default;
}

function estimateMessageTokens(message) {
  if (!message || !message.content) return 0;
  // Rough estimation: ~1.3 tokens per word for English text
  const words = message.content.trim().split(/\\\\s+/).length;
  const chars = message.content.length;
  // More conservative estimate for technical/academic content
  return Math.ceil(words * 1.5 + chars * 0.02);
}

function calculateContextUsage() {
  let totalContextTokens = systemPromptTokens.value;
  
  // Add tokens from all conversation messages
  chatHistory.value.forEach(message => {
    totalContextTokens += estimateMessageTokens(message);
  });
  
  // Add current input if any
  if (messageInput.value.trim()) {
    totalContextTokens += estimateMessageTokens({ content: messageInput.value });
  }
  
  contextTokens.value = totalContextTokens;
  return totalContextTokens;
}

function getContextUsagePercentage() {
  const current = calculateContextUsage();
  const limit = getCurrentContextLimit().limit;
  return Math.min((current / limit) * 100, 100);
}

function getRemainingContextTokens() {
  const current = calculateContextUsage();
  const limit = getCurrentContextLimit().limit;
  return Math.max(limit - current, 0);
}

function getContextUsageColor() {
  const percentage = getContextUsagePercentage();
  if (percentage < 50) return '#10b981'; // Green
  if (percentage < 75) return '#f59e0b'; // Yellow  
  if (percentage < 90) return '#f97316'; // Orange
  return '#ef4444'; // Red
}'''
    
    # Replace the formatNumber function with itself plus the context functions
    content = re.sub(format_number_pattern, r'\1' + context_functions, content, flags=re.DOTALL)
    
    return content

def add_context_window_ui(content):
    """Add context window UI after the session token counter"""
    
    # Find the session token counter section
    token_counter_pattern = r'(<!-- Session Token Counter -->\s*<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">[^<]*<h3[^>]*>📊 Session Tokens</h3>[^<]*(?:<[^>]*>[^<]*)*</div>)'
    
    context_ui = '''
        
        <!-- Context Window Indicator -->
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 class="font-semibold text-green-800 mb-2">💾 Context Window</h3>
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Used:</span>
              <span class="font-mono font-semibold text-green-700">
                {{ formatNumber(calculateContextUsage()) }} / {{ formatNumber(getCurrentContextLimit().limit) }}
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :style="{ 
                  width: getContextUsagePercentage() + '%',
                  backgroundColor: getContextUsageColor()
                }"
              ></div>
            </div>
            <div class="flex justify-between text-xs text-gray-500">
              <span>{{ getContextUsagePercentage().toFixed(1) }}% used</span>
              <span>{{ formatNumber(getRemainingContextTokens()) }} remaining</span>
            </div>
            <div class="text-xs text-gray-500 text-center">
              {{ getCurrentContextLimit().name }}
            </div>
          </div>
        </div>'''
    
    # Add context window UI after session token counter
    content = re.sub(token_counter_pattern, r'\1' + context_ui, content, flags=re.DOTALL)
    
    return content

def add_real_time_updates(content):
    """Add real-time context updates"""
    
    # Find where messages are added to chat history and add context calculation
    message_push_pattern = r'(chatHistory\.value\.push\(\{[^}]*\}\);)'
    
    # Add context calculation after each message push
    context_update = r'\1\n    calculateContextUsage(); // Update context window indicator'
    
    content = re.sub(message_push_pattern, context_update, content)
    
    # Also add update on input change - find the input element
    input_pattern = r'(<textarea[^>]*v-model="messageInput"[^>]*>)'
    input_with_update = r'\1'  # We'll add @input handler
    
    # Add @input handler for real-time updates
    if '@input="adjustTextareaHeight"' in content:
        content = content.replace(
            '@input="adjustTextareaHeight"',
            '@input="adjustTextareaHeight(); calculateContextUsage()"'
        )
    
    return content

def main():
    # Read the current Chat.vue file
    try:
        with open('/Users/simonwang/Documents/Usage/VibeCoding/AItutor_text/src/views/Chat.vue', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: Chat.vue file not found!")
        return
    
    print("📝 Adding context window functionality...")
    
    # Add context window functions
    content = add_context_window_functions(content)
    print("✅ Added context window calculation functions")
    
    # Add context window UI
    content = add_context_window_ui(content)
    print("✅ Added context window UI component")
    
    # Add real-time updates
    content = add_real_time_updates(content)
    print("✅ Added real-time context updates")
    
    # Write the updated content back
    try:
        with open('/Users/simonwang/Documents/Usage/VibeCoding/AItutor_text/src/views/Chat.vue', 'w') as f:
            f.write(content)
        print("✅ Successfully updated Chat.vue with context window indicator!")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()
