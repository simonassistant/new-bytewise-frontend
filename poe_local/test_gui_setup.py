#!/usr/bin/env python3
"""
Test script for Poe GUI setup
Verifies that all components are working correctly.
"""

import os
import sys
import json
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from poe_client import PoeAPIClient
        print("✅ poe_client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import poe_client: {e}")
        return False
    
    try:
        from poe_models_info import PoeModelsInfo
        print("✅ poe_models_info imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import poe_models_info: {e}")
        return False
    
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Flask dependencies: {e}")
        return False
    
    return True

def test_api_key():
    """Test if API key is accessible."""
    print("\n🔑 Testing API key...")
    
    key_file = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync/AItutorDoc/poe/poeKey.md"
    
    if not os.path.exists(key_file):
        print(f"❌ API key file not found: {key_file}")
        return False
    
    try:
        with open(key_file, 'r') as f:
            key = f.read().strip()
            if not key:
                print("❌ API key file is empty")
                return False
            if len(key) < 10:
                print("❌ API key appears to be too short")
                return False
            print("✅ API key file found and appears valid")
            return True
    except Exception as e:
        print(f"❌ Error reading API key: {e}")
        return False

def test_poe_client():
    """Test if Poe client can be initialized."""
    print("\n🤖 Testing Poe client initialization...")
    
    try:
        from poe_client import PoeAPIClient
        client = PoeAPIClient()
        print("✅ Poe client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Poe client: {e}")
        return False

def test_gui_files():
    """Test if GUI files exist."""
    print("\n📁 Testing GUI files...")
    
    required_files = [
        "poe_gui.html",
        "poe_gui_server.py",
        "requirements_gui.txt",
        "README_GUI.md"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            all_exist = False
    
    return all_exist

def test_chat_history_directory():
    """Test if chat history directory exists or can be created."""
    print("\n📚 Testing chat history directory...")
    
    chat_dir = "chatHistory"
    if not os.path.exists(chat_dir):
        try:
            os.makedirs(chat_dir)
            print(f"✅ Created chat history directory: {chat_dir}")
        except Exception as e:
            print(f"❌ Failed to create chat history directory: {e}")
            return False
    else:
        print(f"✅ Chat history directory exists: {chat_dir}")
    
    return True

def run_basic_api_test():
    """Run a basic API test if possible."""
    print("\n🌐 Testing basic API connectivity...")
    
    try:
        from poe_client import PoeAPIClient
        client = PoeAPIClient()
        
        # Try to get balance (this is a lightweight API call)
        balance = client.get_balance()
        if balance:
            print("✅ API connectivity test passed")
            print(f"   Current balance: {balance.get('current_point_balance', 'Unknown')} points")
            return True
        else:
            print("⚠️  API call returned no data (might be normal)")
            return True
            
    except Exception as e:
        print(f"❌ API connectivity test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Poe GUI Setup Test")
    print("=" * 30)
    
    tests = [
        ("Import Test", test_imports),
        ("API Key Test", test_api_key),
        ("Poe Client Test", test_poe_client),
        ("GUI Files Test", test_gui_files),
        ("Chat History Test", test_chat_history_directory),
        ("API Connectivity Test", run_basic_api_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 30)
    print("📊 Test Results Summary:")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The GUI should work correctly.")
        print("\n🚀 To start the GUI, run:")
        print("   python start_gui.py")
        print("   or")
        print("   python poe_gui_server.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Common solutions:")
        print("   - Install dependencies: pip install -r requirements_gui.txt")
        print("   - Check API key configuration")
        print("   - Ensure all files are in the correct directory")

if __name__ == "__main__":
    main()
