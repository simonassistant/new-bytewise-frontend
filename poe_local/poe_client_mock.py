"""
Mock Poe API Client for testing the GUI
This provides a working implementation for testing the chat interface.
"""

import time
import random
from typing import List, Dict, Any, Optional

class PoeAPIClient:
    """Mock client for testing the Poe GUI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the mock Poe API client."""
        self.api_key = api_key or "mock_api_key"
        self.base_url = "https://api.poe.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_balance(self) -> Dict[str, Any]:
        """Get mock balance information."""
        return {
            "current_point_balance": 1110508,
            "expiration_date": "2025-12-31",
            "subscription_type": "Pro"
        }
    
    def send_message(self, message: str, bot_name: str = "GPT-3.5-Turbo", conversation_history: list = None) -> str:
        """
        Send a message and get a mock response with conversation context.
        
        Args:
            message: The message to send
            bot_name: Name of the bot to send message to
            conversation_history: List of previous messages in the conversation
            
        Returns:
            Mock response from the bot
        """
        # Simulate API delay
        time.sleep(0.5)
        
        # If we have conversation history, use it for context
        if conversation_history and len(conversation_history) > 0:
            # Analyze the conversation context
            context = self._analyze_conversation_context(conversation_history, message)
            return self._generate_contextual_response(message, bot_name, context)
        else:
            # First message - generate initial response
            return self._generate_initial_response(message, bot_name)
    
    def _analyze_conversation_context(self, history: list, current_message: str) -> dict:
        """Analyze conversation history to understand context."""
        context = {
            'topic': 'general',
            'mood': 'neutral',
            'previous_questions': [],
            'conversation_length': len(history),
            'last_user_message': '',
            'last_ai_response': ''
        }
        
        # Extract previous user messages and AI responses
        user_messages = [msg for msg in history if msg.get('role') == 'user']
        ai_responses = [msg for msg in history if msg.get('role') == 'assistant']
        
        if user_messages:
            context['last_user_message'] = user_messages[-1].get('content', '')
            context['previous_questions'] = [msg.get('content', '') for msg in user_messages[:-1]]
        
        if ai_responses:
            context['last_ai_response'] = ai_responses[-1].get('content', '')
        
        # Determine topic based on conversation history
        all_text = ' '.join([msg.get('content', '') for msg in history])
        all_text_lower = all_text.lower()
        
        if any(word in all_text_lower for word in ['math', 'calculate', 'number', 'equation']):
            context['topic'] = 'mathematics'
        elif any(word in all_text_lower for word in ['code', 'programming', 'python', 'javascript']):
            context['topic'] = 'programming'
        elif any(word in all_text_lower for word in ['ai', 'artificial', 'intelligence', 'machine']):
            context['topic'] = 'ai'
        elif any(word in all_text_lower for word in ['weather', 'temperature', 'rain', 'sunny']):
            context['topic'] = 'weather'
        elif any(word in all_text_lower for word in ['poem', 'poetry', 'creative', 'write']):
            context['topic'] = 'creative'
        
        return context
    
    def _generate_contextual_response(self, message: str, bot_name: str, context: dict) -> str:
        """Generate a response that considers conversation context."""
        message_lower = message.lower()
        
        # Reference previous conversation
        if context['conversation_length'] > 2:
            if "what did we discuss" in message_lower or "what were we talking about" in message_lower:
                return f"Earlier in our conversation, we discussed {context['topic']}. You asked about {', '.join(context['previous_questions'][-2:]) if context['previous_questions'] else 'various topics'}. How can I help you continue that discussion?"
            
            if "continue" in message_lower or "more" in message_lower:
                if context['topic'] == 'mathematics':
                    return "I'd be happy to continue helping with math! What other mathematical concept would you like to explore?"
                elif context['topic'] == 'programming':
                    return "Let's continue with programming! What coding challenge or concept would you like to work on next?"
                elif context['topic'] == 'ai':
                    return "Great! Let's dive deeper into AI. What specific aspect of artificial intelligence interests you most?"
                else:
                    return f"Absolutely! I'm here to continue our conversation about {context['topic']}. What would you like to explore further?"
        
        # Follow-up questions
        if "?" in message and context['last_ai_response']:
            if "explain" in message_lower:
                return f"Building on what we discussed earlier, let me explain that in more detail. {self._get_topic_explanation(context['topic'])}"
            elif "example" in message_lower:
                return f"Here's a practical example related to our {context['topic']} discussion: {self._get_topic_example(context['topic'])}"
        
        # Acknowledge conversation continuity
        if context['conversation_length'] > 1:
            return f"Continuing our conversation about {context['topic']}, {self._generate_topic_response(message, bot_name, context['topic'])}"
        else:
            return self._generate_initial_response(message, bot_name)
    
    def _generate_initial_response(self, message: str, bot_name: str) -> str:
        """Generate response for first message in conversation."""
        message_lower = message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return f"Hello! I'm {bot_name}. How can I help you today?"
        
        elif "2+2" in message or "2 + 2" in message:
            return "2 + 2 equals 4. This is a basic arithmetic operation where we add two and two together."
        
        elif "what is" in message_lower and "ai" in message_lower:
            return "Artificial Intelligence (AI) is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, and problem-solving."
        
        elif "weather" in message_lower:
            return "I don't have access to real-time weather data, but I'd recommend checking a weather service or app for current conditions in your area."
        
        elif "poem" in message_lower and "coding" in message_lower:
            return """Here's a short poem about coding:

Lines of logic dance in the night,
Functions and loops, a programmer's delight.
Debugging errors, fixing the flow,
Creating solutions that make the world glow.

Code is poetry in motion,
Each line a thoughtful devotion."""

        elif "help" in message_lower:
            return f"I'm {bot_name}, an AI assistant. I can help you with questions, explanations, creative writing, problem-solving, and much more. What would you like to know?"

        elif "thank" in message_lower:
            return "You're very welcome! I'm happy to help. Is there anything else you'd like to know?"

        else:
            responses = [
                f"That's an interesting question! As {bot_name}, I'd be happy to help you explore that topic further. Could you provide more details about what specifically you'd like to know?",
                f"Great question! Let me think about that. As {bot_name}, I can help you understand this better. What aspect would you like me to focus on?",
                f"I appreciate you asking that! As {bot_name}, I'm here to help. Could you tell me more about what you're trying to accomplish?",
                f"That's a thoughtful question! As {bot_name}, I'd love to help you work through this. What's your main goal here?"
            ]
            return random.choice(responses)
    
    def _generate_topic_response(self, message: str, bot_name: str, topic: str) -> str:
        """Generate topic-specific responses."""
        if topic == 'mathematics':
            return "I'd be happy to help with more math problems or concepts. What mathematical topic would you like to explore?"
        elif topic == 'programming':
            return "Let's continue with programming! What coding challenge or language would you like to work on?"
        elif topic == 'ai':
            return "Great! Let's dive deeper into AI concepts. What specific aspect of artificial intelligence would you like to discuss?"
        else:
            return f"I'm here to help you continue exploring {topic}. What would you like to know more about?"
    
    def _get_topic_explanation(self, topic: str) -> str:
        """Get detailed explanation for a topic."""
        explanations = {
            'mathematics': "Mathematics is the study of numbers, shapes, and patterns. It helps us understand the world through logical reasoning and problem-solving.",
            'programming': "Programming is the art of writing instructions for computers. It involves logic, creativity, and problem-solving to create software solutions.",
            'ai': "Artificial Intelligence involves creating systems that can learn, reason, and make decisions. It combines computer science, mathematics, and cognitive science.",
            'creative': "Creative writing is about expressing ideas, emotions, and stories through words. It combines imagination with communication skills.",
            'general': "I'm here to help you explore any topic you're interested in. What would you like to learn about?"
        }
        return explanations.get(topic, explanations['general'])
    
    def _get_topic_example(self, topic: str) -> str:
        """Get practical example for a topic."""
        examples = {
            'mathematics': "For example, if you're learning algebra, we could work on solving equations like 2x + 5 = 13.",
            'programming': "For example, we could write a simple Python function to calculate the factorial of a number.",
            'ai': "For example, we could discuss how machine learning algorithms can recognize patterns in data.",
            'creative': "For example, we could write a short story or poem together, focusing on character development or imagery.",
            'general': "I can provide examples for any topic you'd like to explore. What interests you most?"
        }
        return examples.get(topic, examples['general'])
    
    def get_available_bots(self) -> List[Dict[str, Any]]:
        """Get list of available bots."""
        return [
            {
                "name": "GPT-3.5-Turbo",
                "display_name": "GPT-3.5 Turbo",
                "description": "General-purpose model",
                "points_per_message": 11
            },
            {
                "name": "Claude-Haiku-3", 
                "display_name": "Claude Haiku 3",
                "description": "Fast, affordable model",
                "points_per_message": 17
            },
            {
                "name": "f1-preview",
                "display_name": "F1 Preview", 
                "description": "Ultra-low cost model",
                "points_per_message": 1
            }
        ]

def main():
    """Test the mock client."""
    try:
        client = PoeAPIClient()
        
        print("Testing mock Poe client...")
        
        # Test balance
        balance = client.get_balance()
        print(f"Balance: {balance}")
        
        # Test message
        response = client.send_message("Hello! What is 2+2?", "GPT-3.5-Turbo")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
