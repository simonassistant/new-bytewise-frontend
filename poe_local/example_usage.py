"""
Example usage of the Poe API client.
This script demonstrates how to use the Poe API for various tasks.
"""

from .poe_client import PoeAPIClient
import time

def demonstrate_basic_usage():
    """Demonstrate basic API usage."""
    print("=== Poe API Basic Usage Demo ===\n")
    
    try:
        # Initialize client
        client = PoeAPIClient()
        
        # Check balance
        print("1. Checking API balance...")
        balance = client.get_balance()
        if balance:
            print(f"   Current balance: {balance.get('current_point_balance', 'Unknown')} points")
        else:
            print("   Could not retrieve balance")
        
        print("\n2. Testing message sending...")
        
        # Test different types of messages
        test_messages = [
            "Hello! How are you today?",
            "Can you explain what artificial intelligence is in simple terms?",
            "What's the weather like today?",
            "Can you help me write a short poem about coding?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Test {i}: {message}")
            response = client.send_message(message)
            print(f"   Response: {response}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        print("\n3. Getting available bots...")
        bots = client.get_available_bots()
        if bots:
            print(f"   Found {len(bots)} available bots")
            for bot in bots[:3]:  # Show first 3 bots
                print(f"   - {bot.get('name', 'Unknown')}: {bot.get('description', 'No description')}")
        else:
            print("   Could not retrieve bot list")
            
    except Exception as e:
        print(f"Error in demonstration: {e}")

def demonstrate_educational_use():
    """Demonstrate educational use cases for AI tutoring."""
    print("\n=== Educational Use Cases Demo ===\n")
    
    try:
        client = PoeAPIClient()
        
        # Educational scenarios
        scenarios = [
            {
                "subject": "Mathematics",
                "question": "Can you explain the concept of derivatives in calculus?",
                "follow_up": "Can you give me a simple example?"
            },
            {
                "subject": "Programming",
                "question": "What is object-oriented programming?",
                "follow_up": "Can you show me a simple Python example?"
            },
            {
                "subject": "Science",
                "question": "How does photosynthesis work?",
                "follow_up": "What are the main components involved?"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"Scenario {i}: {scenario['subject']}")
            print(f"Question: {scenario['question']}")
            
            response = client.send_message(scenario['question'])
            print(f"Answer: {response}")
            
            print(f"Follow-up: {scenario['follow_up']}")
            follow_up_response = client.send_message(scenario['follow_up'])
            print(f"Follow-up Answer: {follow_up_response}")
            
            print("-" * 50)
            time.sleep(2)  # Delay between scenarios
            
    except Exception as e:
        print(f"Error in educational demonstration: {e}")

if __name__ == "__main__":
    print("Poe API Example Usage")
    print("=" * 50)
    
    # Run basic usage demo
    demonstrate_basic_usage()
    
    # Run educational use cases demo
    demonstrate_educational_use()
    
    print("\nDemo completed!")
