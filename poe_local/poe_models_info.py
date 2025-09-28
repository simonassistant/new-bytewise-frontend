"""
Poe Models Information and Account Status
This script provides information about available models, pricing, and account status.
"""

import requests
import json
from typing import Dict, List, Any, Optional
try:
    from .poe_client import PoeAPIClient
except ImportError:
    from poe_client import PoeAPIClient

class PoeModelsInfo:
    """Class to get information about Poe models and account status."""
    
    def __init__(self):
        """Initialize with Poe API client."""
        self.client = PoeAPIClient()
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from Poe API.
        
        Returns:
            List of available models with their information
        """
        try:
            # Try to get models from the API
            models = self.client.get_available_bots()
            if models:
                return models
            
            # If API doesn't work, return known models with pricing
            return self.get_known_models_with_pricing()
            
        except Exception as e:
            print(f"Error getting models from API: {e}")
            return self.get_known_models_with_pricing()
    
    def get_known_models_with_pricing(self) -> List[Dict[str, Any]]:
        """
        Get known models with their pricing information.
        
        Returns:
            List of models with pricing data
        """
        models = [
            {
                "name": "f1-preview",
                "display_name": "F1 Preview",
                "points_per_message": 1,
                "description": "Efficient and low-cost model",
                "category": "Text"
            },
            {
                "name": "GPT-3.5-Turbo",
                "display_name": "GPT-3.5 Turbo",
                "points_per_message": 11,
                "description": "General-purpose model",
                "category": "Text"
            },
            {
                "name": "Claude-Haiku-3",
                "display_name": "Claude Haiku 3",
                "points_per_message": 17,
                "description": "Affordable, high-speed model",
                "category": "Text"
            },
            {
                "name": "Gemini-2.0-Flash",
                "display_name": "Gemini 2.0 Flash",
                "points_per_message": 9,
                "description": "Fast, low-cost model",
                "category": "Text"
            },
            {
                "name": "Mistral-Medium",
                "display_name": "Mistral Medium",
                "points_per_message": 218,
                "description": "Mid-range, strong performance",
                "category": "Text"
            },
            {
                "name": "GPT-4o",
                "display_name": "GPT-4o",
                "points_per_message": 224,
                "description": "High-quality, moderate cost",
                "category": "Text"
            },
            {
                "name": "Claude-Sonnet-3.5",
                "display_name": "Claude Sonnet 3.5",
                "points_per_message": 276,
                "description": "Higher cost, strong writing",
                "category": "Text"
            },
            {
                "name": "GPT-4-Turbo",
                "display_name": "GPT-4 Turbo",
                "points_per_message": 378,
                "description": "High cost, long context",
                "category": "Text"
            },
            {
                "name": "Claude-3-Opus",
                "display_name": "Claude 3 Opus",
                "points_per_message": 1697,
                "description": "High cost, deep reasoning",
                "category": "Text"
            },
            {
                "name": "Gemini-2.5-Pro",
                "display_name": "Gemini 2.5 Pro",
                "points_per_message": 716,
                "description": "Advanced Gemini model",
                "category": "Text"
            },
            {
                "name": "Claude-Opus-4",
                "display_name": "Claude Opus 4",
                "points_per_message": 4105,
                "description": "Top-level reasoning, very costly",
                "category": "Text"
            },
            {
                "name": "GPT-5",
                "display_name": "GPT-5",
                "points_per_message": 130,
                "description": "Latest general LLM",
                "category": "Text"
            }
        ]
        
        # Add image generation models
        image_models = [
            {
                "name": "Imagen-4",
                "display_name": "Imagen 4",
                "points_per_message": 328,
                "description": "High-quality image generation",
                "category": "Image"
            },
            {
                "name": "GPT-Image-1",
                "display_name": "GPT Image 1",
                "points_per_message": 328,
                "description": "GPT-powered image generation",
                "category": "Image"
            },
            {
                "name": "Flux-Kontext",
                "display_name": "Flux Kontext",
                "points_per_message": 200,
                "description": "Advanced image generation",
                "category": "Image"
            },
            {
                "name": "Seedream-3.0",
                "display_name": "Seedream 3.0",
                "points_per_message": 150,
                "description": "Creative image generation",
                "category": "Image"
            }
        ]
        
        # Add video generation models
        video_models = [
            {
                "name": "Veo-3",
                "display_name": "Veo 3",
                "points_per_message": 500,
                "description": "High-quality video generation",
                "category": "Video"
            },
            {
                "name": "Runway-Gen-4-Turbo",
                "display_name": "Runway Gen 4 Turbo",
                "points_per_message": 400,
                "description": "Advanced video generation",
                "category": "Video"
            }
        ]
        
        # Add audio generation models
        audio_models = [
            {
                "name": "Kling-2.1",
                "display_name": "Kling 2.1",
                "points_per_message": 300,
                "description": "Audio generation model",
                "category": "Audio"
            },
            {
                "name": "ElevenLabs",
                "display_name": "ElevenLabs",
                "points_per_message": 50,
                "description": "High-quality voice synthesis",
                "category": "Audio"
            },
            {
                "name": "Lyria",
                "display_name": "Lyria",
                "points_per_message": 100,
                "description": "Music generation",
                "category": "Audio"
            }
        ]
        
        return models + image_models + video_models + audio_models
    
    def get_account_status(self) -> Dict[str, Any]:
        """
        Get account status including balance and expiration.
        
        Returns:
            Dictionary with account information
        """
        try:
            balance_info = self.client.get_balance()
            return balance_info
        except Exception as e:
            print(f"Error getting account status: {e}")
            return {}
    
    def display_models_by_category(self, models: List[Dict[str, Any]]):
        """Display models organized by category."""
        categories = {}
        
        # Group models by category
        for model in models:
            category = model.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(model)
        
        # Display each category
        for category, category_models in categories.items():
            print(f"\n{'='*20} {category.upper()} MODELS {'='*20}")
            print(f"{'Model Name':<25} {'Points':<10} {'Description'}")
            print("-" * 70)
            
            # Sort by points
            category_models.sort(key=lambda x: x.get('points_per_message', 0))
            
            for model in category_models:
                name = model.get('display_name', model.get('name', 'Unknown'))
                points = model.get('points_per_message', 0)
                description = model.get('description', 'No description')
                
                print(f"{name:<25} {points:<10} {description}")
    
    def display_account_info(self, account_info: Dict[str, Any]):
        """Display account information."""
        print(f"\n{'='*20} ACCOUNT STATUS {'='*20}")
        
        if not account_info:
            print("❌ Could not retrieve account information")
            return
        
        # Display balance information
        balance = account_info.get('current_point_balance', 'Unknown')
        print(f"💰 Current Point Balance: {balance}")
        
        # Display expiration information
        expiration = account_info.get('expiration_date', 'Unknown')
        if expiration != 'Unknown':
            print(f"📅 Expiration Date: {expiration}")
        
        # Display subscription information
        subscription = account_info.get('subscription_type', 'Unknown')
        if subscription != 'Unknown':
            print(f"📋 Subscription Type: {subscription}")
        
        # Display daily/monthly limits
        daily_limit = account_info.get('daily_point_limit', 'Unknown')
        if daily_limit != 'Unknown':
            print(f"📊 Daily Point Limit: {daily_limit}")
        
        monthly_limit = account_info.get('monthly_point_limit', 'Unknown')
        if monthly_limit != 'Unknown':
            print(f"📊 Monthly Point Limit: {monthly_limit}")
    
    def get_subscription_plans(self) -> List[Dict[str, Any]]:
        """Get information about subscription plans."""
        plans = [
            {
                "name": "Free Tier",
                "price": "$0",
                "points": "Daily free points",
                "description": "Limited daily points, resets every 24 hours"
            },
            {
                "name": "Basic",
                "price": "$4.99/month",
                "points": "10,000 points/day",
                "description": "Good for light usage"
            },
            {
                "name": "Standard",
                "price": "$19.99/month",
                "points": "1,000,000 points/month",
                "description": "Moderate usage"
            },
            {
                "name": "Pro",
                "price": "$49.99/month",
                "points": "2,500,000 points/month",
                "description": "Heavy usage"
            },
            {
                "name": "Enterprise",
                "price": "$99.99/month",
                "points": "5,000,000 points/month",
                "description": "High-volume usage"
            },
            {
                "name": "Ultimate",
                "price": "$249.99/month",
                "points": "12,500,000 points/month",
                "description": "Maximum usage"
            }
        ]
        return plans
    
    def display_subscription_plans(self, plans: List[Dict[str, Any]]):
        """Display subscription plans."""
        print(f"\n{'='*20} SUBSCRIPTION PLANS {'='*20}")
        print(f"{'Plan':<15} {'Price':<15} {'Points':<20} {'Description'}")
        print("-" * 80)
        
        for plan in plans:
            name = plan.get('name', 'Unknown')
            price = plan.get('price', 'Unknown')
            points = plan.get('points', 'Unknown')
            description = plan.get('description', 'No description')
            
            print(f"{name:<15} {price:<15} {points:<20} {description}")
    
    def run_full_report(self):
        """Run a complete report of models, pricing, and account status."""
        print("🤖 POE MODELS AND ACCOUNT INFORMATION")
        print("=" * 50)
        
        # Get and display models
        print("\n📋 Fetching available models...")
        models = self.get_available_models()
        self.display_models_by_category(models)
        
        # Get and display account status
        print("\n📊 Checking account status...")
        account_info = self.get_account_status()
        self.display_account_info(account_info)
        
        # Display subscription plans
        plans = self.get_subscription_plans()
        self.display_subscription_plans(plans)
        
        print(f"\n{'='*50}")
        print("✅ Report completed!")

def main():
    """Main function to run the models info report."""
    try:
        info = PoeModelsInfo()
        info.run_full_report()
    except Exception as e:
        print(f"Error running report: {e}")

if __name__ == "__main__":
    main()
