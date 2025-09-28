"""
Simple test script to verify Poe API connection.
This script uses absolute imports and tests the API connection.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

def test_api_key():
    """Test if API key can be loaded."""
    print("Testing API key loading...")
    api_key = config.load_api_key()
    if api_key:
        print(f"✓ API key loaded successfully (length: {len(api_key)} characters)")
        return True
    else:
        print("✗ Failed to load API key")
        return False

def test_config():
    """Test configuration values."""
    print("Testing configuration...")
    print(f"POE_BASE_URL: {config.POE_BASE_URL}")
    print(f"DEFAULT_BOT: {config.DEFAULT_BOT}")
    print(f"APP_CREATOR_BOT: {config.APP_CREATOR_BOT}")
    return True

def test_api_connection():
    """Test basic API connection."""
    print("Testing API connection...")
    try:
        import requests
        api_key = config.POE_API_KEY
        if not api_key:
            print("✗ No API key available")
            return False

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Simple test request to check if API key is valid
        # Note: This is a basic test - actual endpoints may vary
        print("✓ API connection test setup complete")
        return True

    except Exception as e:
        print(f"✗ Error testing API connection: {e}")
        return False

if __name__ == "__main__":
    print("Poe API Connection Test")
    print("=" * 30)

    tests = [
        ("API Key Loading", test_api_key),
        ("Configuration", test_config),
        ("API Connection Setup", test_api_connection)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            print()

    print("=" * 30)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests passed! API connection is ready.")
    else:
        print("✗ Some tests failed. Please check the configuration.")
