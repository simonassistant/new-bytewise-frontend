#!/usr/bin/env python3
"""
Poe GUI Launcher
Simple script to start the Poe chat GUI with proper setup.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def check_api_key():
    """Check if Poe API key is configured."""
    key_file = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync/AItutorDoc/poe/poeKey.md"
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                key = f.read().strip()
                if key and len(key) > 10:
                    print("✅ Poe API key found")
                    return True
        except Exception as e:
            print(f"❌ Error reading API key: {e}")
    else:
        print(f"❌ API key file not found at: {key_file}")
    
    print("Please ensure your Poe API key is properly configured.")
    return False

def start_server():
    """Start the Flask server."""
    print("🚀 Starting Poe GUI Server...")
    print("📱 The interface will open in your browser automatically")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the server
        subprocess.run([sys.executable, "poe_gui_server.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main launcher function."""
    print("🤖 Poe Models Chat GUI Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("poe_gui_server.py"):
        print("❌ Please run this script from the poe_local directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Cannot proceed without dependencies")
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        print("❌ Cannot proceed without valid API key")
        sys.exit(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
