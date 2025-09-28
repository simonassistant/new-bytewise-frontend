"""
Test script to verify all API endpoints are working correctly.
"""

import requests
import json
import time

API_BASE = "http://localhost:5001/api"

def test_health():
    """Test health endpoint."""
    print("Testing /api/health...")
    try:
        response = requests.get(f"{API_BASE}/health")
        data = response.json()
        print(f"✓ Health check: {data}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_chat():
    """Test chat endpoint."""
    print("\nTesting /api/chat...")
    try:
        payload = {
            "message": "Hello, can you help me with Vue.js development?",
            "bot": "App-Creator"
        }
        response = requests.post(f"{API_BASE}/chat", json=payload)
        data = response.json()
        print(f"✓ Chat response: {data}")
        return True
    except Exception as e:
        print(f"✗ Chat test failed: {e}")
        return False

def test_create_app():
    """Test create app endpoint."""
    print("\nTesting /api/create-app...")
    try:
        payload = {
            "description": "A simple todo list application with Vue.js",
            "type": "web_app",
            "framework": "vue"
        }
        response = requests.post(f"{API_BASE}/create-app", json=payload)
        data = response.json()
        print(f"✓ Create app response: {data}")
        return True
    except Exception as e:
        print(f"✗ Create app test failed: {e}")
        return False

def test_review_code():
    """Test code review endpoint."""
    print("\nTesting /api/review-code...")
    try:
        payload = {
            "code": "const message = 'Hello World'; console.log(message);",
            "language": "javascript"
        }
        response = requests.post(f"{API_BASE}/review-code", json=payload)
        data = response.json()
        print(f"✓ Code review response: {data}")
        return True
    except Exception as e:
        print(f"✗ Code review test failed: {e}")
        return False

def test_generate_component():
    """Test component generation endpoint."""
    print("\nTesting /api/generate-component...")
    try:
        payload = {
            "description": "A responsive navigation bar with hamburger menu",
            "framework": "vue"
        }
        response = requests.post(f"{API_BASE}/generate-component", json=payload)
        data = response.json()
        print(f"✓ Generate component response: {data}")
        return True
    except Exception as e:
        print(f"✗ Generate component test failed: {e}")
        return False

def test_get_bots():
    """Test get bots endpoint."""
    print("\nTesting /api/bots...")
    try:
        response = requests.get(f"{API_BASE}/bots")
        data = response.json()
        print(f"✓ Bots list: {data}")
        return True
    except Exception as e:
        print(f"✗ Get bots test failed: {e}")
        return False

if __name__ == "__main__":
    print("Poe API Endpoints Test")
    print("=" * 40)

    tests = [
        ("Health Check", test_health),
        ("Chat", test_chat),
        ("Create App", test_create_app),
        ("Review Code", test_review_code),
        ("Generate Component", test_generate_component),
        ("Get Bots", test_get_bots)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")

    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All API endpoints are working correctly!")
    else:
        print("✗ Some endpoints failed. Check the server logs.")
