"""
Flask API server to connect Vue.js frontend with Poe App Creator.
This server provides RESTful endpoints for your frontend to interact with Poe's App Creator.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simple_app_creator import PoeAppCreatorClient

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue.js frontend

# Initialize the Poe client
try:
    poe_client = PoeAppCreatorClient()
    print("✓ Poe App Creator client initialized successfully")
except Exception as e:
    print(f"✗ Error initializing Poe client: {e}")
    poe_client = None

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Poe App Creator API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
            .method { color: #007bff; font-weight: bold; }
            .status { padding: 10px; border-radius: 5px; margin: 20px 0; }
            .healthy { background-color: #d4edda; color: #155724; }
            .error { background-color: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Poe App Creator API Server</h1>
            <div class="status healthy">
                ✅ Server is running on port 5001
            </div>
            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <span class="method">GET</span> /api/health - Health check
            </div>
            <div class="endpoint">
                <span class="method">POST</span> /api/chat - Send message to Poe App Creator
            </div>
            <div class="endpoint">
                <span class="method">POST</span> /api/create-app - Create application
            </div>
            <div class="endpoint">
                <span class="method">POST</span> /api/review-code - Get code review
            </div>
            <div class="endpoint">
                <span class="method">POST</span> /api/generate-component - Generate component
            </div>
            <div class="endpoint">
                <span class="method">GET</span> /api/bots - Get available bots
            </div>
            <h2>Usage:</h2>
            <p>This API server provides a bridge between your Vue.js frontend and Poe's App Creator bot.</p>
            <p>Access your Vue.js application to use the graphical interface, or make direct API calls to these endpoints.</p>
            <h2>Test:</h2>
            <p><a href="/api/health" target="_blank">Click here to test the health endpoint</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Poe App Creator API",
        "client_status": "ready" if poe_client else "error"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to Poe App Creator."""
    try:
        if not poe_client:
            return jsonify({"error": "Poe client not initialized"}), 500

        data = request.get_json()
        message = data.get('message', '')
        bot_name = data.get('bot', 'App-Creator')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        response = poe_client.send_message(message, bot_name)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create-app', methods=['POST'])
def create_app():
    """Create an app using Poe App Creator."""
    try:
        if not poe_client:
            return jsonify({"error": "Poe client not initialized"}), 500

        data = request.get_json()
        app_description = data.get('description', '')
        app_type = data.get('type', 'web_app')
        framework = data.get('framework', 'vue')

        if not app_description:
            return jsonify({"error": "App description is required"}), 400

        response = poe_client.create_app_request(app_description, app_type, framework)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/review-code', methods=['POST'])
def review_code():
    """Get code review from Poe App Creator."""
    try:
        if not poe_client:
            return jsonify({"error": "Poe client not initialized"}), 500

        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'javascript')

        if not code:
            return jsonify({"error": "Code is required"}), 400

        response = poe_client.get_code_review(code, language)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-component', methods=['POST'])
def generate_component():
    """Generate a component using Poe App Creator."""
    try:
        if not poe_client:
            return jsonify({"error": "Poe client not initialized"}), 500

        data = request.get_json()
        description = data.get('description', '')
        framework = data.get('framework', 'vue')

        if not description:
            return jsonify({"error": "Component description is required"}), 400

        response = poe_client.generate_component(description, framework)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bots', methods=['GET'])
def get_bots():
    """Get available bots information."""
    return jsonify({
        "bots": [
            {
                "name": "App-Creator",
                "description": "Helps create applications and components",
                "capabilities": ["app_creation", "code_review", "component_generation"]
            },
            {
                "name": "GPT-3.5-Turbo",
                "description": "General purpose AI assistant",
                "capabilities": ["general_chat", "coding_help"]
            }
        ]
    })

if __name__ == '__main__':
    print("Starting Poe App Creator API Server...")
    print("API Endpoints:")
    print("  GET  /api/health - Health check")
    print("  POST /api/chat - Send message to Poe")
    print("  POST /api/create-app - Create application")
    print("  POST /api/review-code - Get code review")
    print("  POST /api/generate-component - Generate component")
    print("  GET  /api/bots - Get available bots")
    print("\nServer starting on http://localhost:5001...")

    app.run(host='0.0.0.0', port=5001, debug=True)
