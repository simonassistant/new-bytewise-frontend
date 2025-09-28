"""
Poe API Package for AI Tutor Development
This package provides a comprehensive interface to interact with the Poe API.
"""

from .poe_client import PoeAPIClient
from .poe_models_info import PoeModelsInfo
from .config import POE_API_KEY, POE_BASE_URL, DEFAULT_BOT, REQUEST_DELAY, MAX_RETRIES

__version__ = "1.0.0"
__author__ = "AI Tutor Development Team"

__all__ = [
    'PoeAPIClient',
    'PoeModelsInfo', 
    'POE_API_KEY',
    'POE_BASE_URL',
    'DEFAULT_BOT',
    'REQUEST_DELAY',
    'MAX_RETRIES'
]
