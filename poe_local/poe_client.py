"""
Poe API Client for AI Tutor Development
This module provides a simple interface to interact with the Poe API.
"""

import os
import requests
from typing import List, Dict, Any, Optional
try:
    from .config import POE_API_KEY, POE_BASE_URL, DEFAULT_BOT, REQUEST_DELAY, MAX_RETRIES
except ImportError:
    from config import POE_API_KEY, POE_BASE_URL, DEFAULT_BOT, REQUEST_DELAY, MAX_RETRIES

class PoeAPIClient:
    """Client for interacting with the Poe API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Poe API client.
        
        Args:
            api_key: Poe API key. If not provided, will try to load from environment.
        """
        self.api_key = api_key or POE_API_KEY
        if not self.api_key:
            raise ValueError("Poe API key not found. Please check that the key file exists at /Users/simonwang/Documents/Usage/ObSync/Vault4sync/AItutorDoc/poeKey.md")
        
        self.base_url = POE_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current point balance.
        
        Returns:
            Dictionary containing balance information.
        """
        try:
            response = requests.get(
                f"{self.base_url}/usage/current_balance",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching balance: {e}")
            return {}
    
    def send_message(self, message: str, bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a message to a Poe bot and get response.
        
        Args:
            message: The message to send
            bot_name: Name of the bot to send message to
            
        Returns:
            Response from the bot
        """
        try:
            # Use OpenAI-compatible endpoint
            payload = {
                "model": bot_name,
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            return f"Error sending message: {e}"
        except KeyError as e:
            return f"Error parsing response: {e}"
    
    def get_available_bots(self) -> List[Dict[str, Any]]:
        """
        Get list of available bots.
        
        Returns:
            List of available bots
        """
        try:
            response = requests.get(
                f"{self.base_url}/bots",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('bots', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching bots: {e}")
            return []


def main():
    """Example usage of the Poe API client."""
    try:
        # Initialize the client
        client = PoeAPIClient()
        
        # Check balance
        print("Checking balance...")
        balance = client.get_balance()
        print(f"Current balance: {balance}")
        
        # Send a test message
        print("\nSending test message...")
        response = client.send_message("Hello! Can you help me with a simple math problem? What is 2+2?")
        print(f"Bot response: {response}")
        
        # Get available bots
        print("\nFetching available bots...")
        bots = client.get_available_bots()
        print(f"Available bots: {len(bots)} found")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
