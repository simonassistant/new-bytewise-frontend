from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.routers.streaming_avatar import streaming_avatar, register_socketio_handlers
from app.routers.chatbot import chatbot
from app.routers.openrouter import openrouter
from app.routers.database import database
from dotenv import load_dotenv
load_dotenv()
# Create Flask app
app = Flask(__name__)

# --- Enable CORS for REST API ---
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(streaming_avatar, url_prefix="/api/streaming-avatar")
app.register_blueprint(chatbot, url_prefix="/api/chatbot")  # this is hkbu chatbot
app.register_blueprint(
    openrouter, url_prefix="/api/openrouter"
)  # this is openrouter chatbot
app.register_blueprint(database, url_prefix="/api/db")

# Initialize SocketIO with eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register websocket event handlers
register_socketio_handlers(socketio)

if __name__ == "__main__":
    # Run on port 8000 to avoid conflict with frontend on port 5000
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
