"""
Flask server for Poe GUI Chat Interface
This server provides the backend API for the web-based chat interface.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path
from poe_client_mock import PoeAPIClient
from poe_models_info import PoeModelsInfo

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Poe client
try:
    poe_client = PoeAPIClient()
    models_info = PoeModelsInfo()
    print("✅ Poe API client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Poe API client: {e}")
    poe_client = None
    models_info = None

# Setup chat history directory
CHAT_HISTORY_DIR = Path(__file__).parent / "chatHistory"
CHAT_HISTORY_DIR.mkdir(exist_ok=True)
print(f"📁 Chat history directory: {CHAT_HISTORY_DIR}")

def save_chat_to_file(chat_data):
    """Save chat data to a JSON file."""
    try:
        chat_id = chat_data.get('id', f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        filename = f"{chat_id}.json"
        filepath = CHAT_HISTORY_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Chat saved to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error saving chat to file: {e}")
        return False

def load_chat_from_file(chat_id):
    """Load chat data from a JSON file."""
    try:
        filename = f"{chat_id}.json"
        filepath = CHAT_HISTORY_DIR / filename
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading chat from file: {e}")
        return None

def get_all_chat_files():
    """Get all chat files from the directory."""
    try:
        chat_files = []
        for file_path in CHAT_HISTORY_DIR.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                    chat_data['filename'] = file_path.name
                    chat_files.append(chat_data)
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                continue
        
        # Sort by timestamp (newest first)
        chat_files.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return chat_files
    except Exception as e:
        print(f"❌ Error getting chat files: {e}")
        return []

def delete_chat_file(chat_id):
    """Delete a chat file."""
    try:
        filename = f"{chat_id}.json"
        filepath = CHAT_HISTORY_DIR / filename
        
        if filepath.exists():
            filepath.unlink()
            print(f"🗑️ Deleted chat file: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error deleting chat file: {e}")
        return False

@app.route('/')
def serve_gui():
    """Serve the main GUI HTML file."""
    return send_from_directory(os.path.dirname(__file__), 'poe_gui.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        model = data.get('model', 'GPT-3.5-Turbo')
        save_to_server = data.get('save_to_server', False)
        chat_id = data.get('chat_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not poe_client:
            return jsonify({'error': 'Poe API client not initialized'}), 500
        
        # Get conversation history if provided
        conversation_history = data.get('conversation_history', [])
        
        # Send message to Poe API with conversation context
        response = poe_client.send_message(message, model, conversation_history)
        
        result = {
            'response': response,
            'model': model,
            'timestamp': datetime.now().isoformat()
        }
        
        # If this is a save request, save the chat to server
        if save_to_server and chat_id:
            chat_data = {
                'id': chat_id,
                'title': data.get('title', message[:50] + '...' if len(message) > 50 else message),
                'model': model,
                'timestamp': datetime.now().isoformat(),
                'messages': data.get('messages', [])
            }
            
            # Add the current message and response
            chat_data['messages'].append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            chat_data['messages'].append({
                'role': 'assistant', 
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            if save_chat_to_file(chat_data):
                result['saved_to_server'] = True
                result['chat_id'] = chat_id
            else:
                result['saved_to_server'] = False
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models."""
    try:
        if models_info:
            models = models_info.get_available_models()
            return jsonify({'models': models})
        else:
            # Return basic model list if models_info is not available
            basic_models = [
                {"name": "GPT-3.5-Turbo", "display_name": "GPT-3.5 Turbo", "points_per_message": 11},
                {"name": "Claude-Haiku-3", "display_name": "Claude Haiku 3", "points_per_message": 17},
                {"name": "Gemini-2.0-Flash", "display_name": "Gemini 2.0 Flash", "points_per_message": 9},
                {"name": "GPT-4o", "display_name": "GPT-4o", "points_per_message": 224},
                {"name": "Claude-Sonnet-3.5", "display_name": "Claude Sonnet 3.5", "points_per_message": 276},
                {"name": "Mistral-Medium", "display_name": "Mistral Medium", "points_per_message": 218},
                {"name": "f1-preview", "display_name": "F1 Preview", "points_per_message": 1}
            ]
            return jsonify({'models': basic_models})
    except Exception as e:
        print(f"Error getting models: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/balance', methods=['GET'])
def get_balance():
    """Get current account balance."""
    try:
        if not poe_client:
            return jsonify({'error': 'Poe API client not initialized'}), 500
        
        balance = poe_client.get_balance()
        return jsonify(balance)
        
    except Exception as e:
        print(f"Error getting balance: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'poe_client_initialized': poe_client is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    """Get chat history from server storage."""
    try:
        chat_files = get_all_chat_files()
        return jsonify({'history': chat_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-history', methods=['POST'])
def save_chat_history():
    """Save chat history to server storage."""
    try:
        data = request.get_json()
        chat_id = data.get('id')
        
        if not chat_id:
            return jsonify({'error': 'Chat ID is required'}), 400
        
        if save_chat_to_file(data):
            return jsonify({'status': 'saved', 'chat_id': chat_id})
        else:
            return jsonify({'error': 'Failed to save chat'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-history/<chat_id>', methods=['GET'])
def get_single_chat(chat_id):
    """Get a specific chat by ID."""
    try:
        chat_data = load_chat_from_file(chat_id)
        if chat_data:
            return jsonify(chat_data)
        else:
            return jsonify({'error': 'Chat not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-history/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """Delete a specific chat by ID."""
    try:
        if delete_chat_file(chat_id):
            return jsonify({'status': 'deleted', 'chat_id': chat_id})
        else:
            return jsonify({'error': 'Chat not found or could not be deleted'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Poe GUI Server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔧 Make sure your Poe API key is configured correctly")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
