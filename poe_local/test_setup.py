"""
Test script to verify Poe API setup.
This script tests the API key loading and basic functionality.
"""

def test_api_key_loading():
    """Test that the API key is loaded correctly."""
    print("Testing API key loading...")
    
    try:
        from .config import POE_API_KEY
        
        if POE_API_KEY:
            print(f"✓ API key loaded successfully (length: {len(POE_API_KEY)} characters)")
            print(f"✓ Key starts with: {POE_API_KEY[:10]}...")
            return True
        else:
            print("✗ API key is empty or None")
            return False
            
    except Exception as e:
        print(f"✗ Error loading API key: {e}")
        return False

def test_client_initialization():
    """Test that the Poe client can be initialized."""
    print("\nTesting client initialization...")
    
    try:
        from .poe_client import PoeAPIClient
        
        client = PoeAPIClient()
        print("✓ PoeAPIClient initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
        return False

def test_api_connection():
    """Test basic API connection."""
    print("\nTesting API connection...")
    
    try:
        from .poe_client import PoeAPIClient
        
        client = PoeAPIClient()
        
        # Test balance check
        balance = client.get_balance()
        if balance:
            print("✓ API connection successful")
            print(f"  Balance info: {balance}")
            return True
        else:
            print("✗ API connection failed - no balance data received")
            return False
            
    except Exception as e:
        print(f"✗ Error testing API connection: {e}")
        return False

def main():
    """Run all tests."""
    print("Poe API Setup Test")
    print("=" * 30)
    
    tests = [
        test_api_key_loading,
        test_client_initialization,
        test_api_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 30)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Poe API setup is working correctly.")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    main()
