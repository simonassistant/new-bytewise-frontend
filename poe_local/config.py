"""
Configuration file for Poe API access.
This file loads the API key from an external file for security.
"""

import os

def load_api_key():
    """Load API key from external file."""
    key_file_path = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync/WritingBotDev/technical/poe/poeKey.md"
    try:
        with open(key_file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Warning: API key file not found at {key_file_path}")
        return None
    except Exception as e:
        print(f"Error reading API key: {e}")
        return None

# Poe API Configuration
POE_API_KEY = load_api_key()

# API Settings
POE_BASE_URL = "https://api.poe.com"
DEFAULT_BOT = "GPT-3.5-Turbo"

# App Creator Configuration
APP_CREATOR_BOT = "App-Creator"

# Rate limiting settings
REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3
