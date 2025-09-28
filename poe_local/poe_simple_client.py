"""
Simple Poe API Client using the poe-api package.
This client provides a straightforward interface to interact with Poe.
"""

import asyncio
from typing import List, Dict, Any, Optional
from .config import POE_API_KEY

class PoeSimpleClient:
    """Simple client for interacting with the Poe API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Poe API client.
        
        Args:
            api_key: Poe API key. If not provided, will load from config.
        """
        self.api_key = api_key or POE_API_KEY
        if not self.api_key:
            raise ValueError("Poe API key not found. Please check your config.py file.")
        
        # Import poe-api here to avoid import errors if not installed
        try:
            from poe import Client
            self.client = Client()
        except ImportError:
            raise ImportError("poe-api package not installed. Run: pip install poe-api")
    
    async def send_message(self, message: str, bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a message to a Poe bot and get response.
        
        Args:
            message: The message to send
            bot_name: Name of the bot to send message to
            
        Returns:
            Response from the bot
        """
        try:
            # Note: This is a simplified implementation
            # The actual poe-api package might have different methods
            response = await self.client.send_message(bot_name, message)
            return response
        except Exception as e:
            return f"Error sending message: {e}"
    
    async def get_available_bots(self) -> List[Dict[str, Any]]:
        """
        Get list of available bots.
        
        Returns:
            List of available bots
        """
        try:
            # This would need to be implemented based on the actual poe-api package
            return []
        except Exception as e:
            print(f"Error fetching bots: {e}")
            return []
    
    def send_message_sync(self, message: str, bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Synchronous version of send_message.
        
        Args:
            message: The message to send
            bot_name: Name of the bot to send message to
            
        Returns:
            Response from the bot
        """
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.send_message(message, bot_name))
        except Exception as e:
            return f"Error sending message: {e}"

def main():
    """Example usage of the simple Poe API client."""
    try:
        client = PoeSimpleClient()
        
        # Send a test message
        print("Sending test message...")
        response = client.send_message_sync("Hello! Can you help me with a simple math problem? What is 2+2?")
        print(f"Bot response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
