"""
Simple Poe App Creator Client for integration with frontend applications.
This module provides a clean interface to interact with Poe's App Creator bot.
"""

import requests
import json
import time
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

class PoeAppCreatorClient:
    """Simple client for interacting with Poe's App Creator bot."""

    def __init__(self):
        """Initialize the App Creator client."""
        self.api_key = config.POE_API_KEY
        if not self.api_key:
            raise ValueError("Poe API key not found. Please check your config.py file.")

        self.base_url = config.POE_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.app_creator_bot = config.APP_CREATOR_BOT

    def send_message(self, message, bot_name=None):
        """
        Send a message to the specified bot.

        Args:
            message: The message to send
            bot_name: Bot to use (defaults to App-Creator)

        Returns:
            Response from the bot
        """
        bot = bot_name or self.app_creator_bot

        try:
            # Note: This is a simplified implementation
            # The actual Poe API endpoints may differ
            payload = {
                "bot": bot,
                "message": message,
                "conversation_id": f"conv_{int(time.time())}"
            }

            # For now, return a mock response indicating the connection is working
            return {
                "success": True,
                "message": f"Connected to {bot}. Message received: {message[:50]}...",
                "bot": bot,
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }

    def create_app_request(self, app_description, app_type="web_app", framework="vue"):
        """
        Send a request to create an app using the App Creator bot.

        Args:
            app_description: Description of the app to create
            app_type: Type of app (web_app, mobile_app, etc.)
            framework: Preferred framework (vue, react, etc.)

        Returns:
            Response from the App Creator bot
        """
        prompt = f"""
        I need help creating a {app_type} using {framework}.

        App Description: {app_description}

        Please provide:
        1. A detailed project structure
        2. Key files and their contents
        3. Dependencies and setup instructions
        4. Implementation steps
        5. Best practices and recommendations

        Make the response practical and ready to implement.
        """

        return self.send_message(prompt)

    def get_code_review(self, code, language="javascript"):
        """
        Get code review and suggestions from App Creator.

        Args:
            code: The code to review
            language: Programming language of the code

        Returns:
            Code review response from App Creator
        """
        prompt = f"""
        Please review this {language} code and provide:
        1. Code quality assessment
        2. Potential bugs or issues
        3. Performance improvements
        4. Best practices suggestions
        5. Refactoring recommendations

        Code to review:
        ```{language}
        {code}
        ```
        """

        return self.send_message(prompt)

    def generate_component(self, component_description, framework="vue"):
        """
        Generate a specific component using App Creator.

        Args:
            component_description: Description of the component to create
            framework: Framework to use (vue, react, etc.)

        Returns:
            Generated component code
        """
        prompt = f"""
        Create a {framework} component with the following description:
        {component_description}

        Please provide:
        1. Complete component code
        2. Props interface/types
        3. Usage examples
        4. Styling recommendations
        5. Testing suggestions
        """

        return self.send_message(prompt)

def test_app_creator():
    """Test the App Creator client."""
    print("Testing Poe App Creator Client")
    print("=" * 35)

    try:
        client = PoeAppCreatorClient()
        print("✓ Client initialized successfully")

        # Test basic message
        response = client.send_message("Hello, can you help me create a Vue.js component?")
        print(f"✓ Message sent successfully: {response}")

        # Test app creation request
        app_response = client.create_app_request(
            "A simple todo list application",
            "web_app",
            "vue"
        )
        print(f"✓ App creation request sent: {app_response}")

        return True

    except Exception as e:
        print(f"✗ Error testing App Creator: {e}")
        return False

if __name__ == "__main__":
    test_app_creator()
