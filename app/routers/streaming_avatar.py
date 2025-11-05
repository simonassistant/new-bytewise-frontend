from flask import Blueprint, jsonify, Response
import re, os, requests
from flask_socketio import emit, SocketIO
from app.routers.chatbot import (
    chat_completion,
    preprocess_chat_history,
    chat_completion_openrouter,
)
from dotenv import load_dotenv

load_dotenv()
streaming_avatar = Blueprint("streaming_avatar", __name__)


@streaming_avatar.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module streaming_avatar"})


@streaming_avatar.route("/get-speech-token", methods=["GET"])
def get_speech_token():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = "eastasia"
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        token_response = requests.post(
            f"https://{speech_region}.api.cognitive.microsoft.com/sts/v1.0/issueToken",
            headers=headers,
        )
        token_response.raise_for_status()
        return jsonify({"token": token_response.text, "region": speech_region})
    except requests.exceptions.RequestException:
        return Response("There was an error authorizing your speech key.", status=401)


socket_namespace = "/api/streaming-avatar"


# Helper: remove emojis (covers most ranges)
def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map
        "\U0001f700-\U0001f77f"  # alchemical
        "\U0001f780-\U0001f7ff"  # geometric shapes extended
        "\U0001f800-\U0001f8ff"  # supplemental arrows
        "\U0001f900-\U0001f9ff"  # supplemental symbols
        "\U0001fa00-\U0001fa6f"  # chess, symbols
        "\U0001fa70-\U0001faff"  # symbols & pictographs extended-A
        "\U00002702-\U000027b0"  # dingbats
        "\U000024c2-\U0001f251"  # Enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def register_socketio_handlers(socketio: SocketIO):
    @socketio.on("connect", namespace=socket_namespace)
    def handle_connect():
        print("✅ Client connected to /streaming-avatar")
        emit("message", {"info": "Connected to WebSocket!"})

    @socketio.on("disconnect", namespace=socket_namespace)
    def handle_disconnect():
        print("⚠️ Client disconnected from /streaming-avatar")

    @socketio.on("user_message", namespace=socket_namespace)
    def handle_user_message(data):
        """Chat → Assistant reply → in-memory MP3 audio streaming."""
        try:
            chat_history = data.get("history", [])
            api_key = data.get("api_key")
            model_name = data.get("model", "gpt-4")
            system_prompt = data.get("system_prompt", "")
            top_p = data.get("top_p", 1.0)
            provider = data.get("provider", "hkbu")

            # ---- Chat completion ----
            preprocessed_history = preprocess_chat_history(
                [
                    {
                        "role": "system",
                        "content": "Do not reply in markdown, and do not reply any code, do not use bold text. Keep your reply short. Also follow these instructions: "
                        + system_prompt,
                    }
                ]
                + chat_history
            )

            if provider == "openrouter":
                result = chat_completion_openrouter(
                    chat_history=preprocessed_history,
                    model_name=model_name,
                )
            else:  # default to HKBU GenAI
                result = chat_completion(
                    chat_history=preprocessed_history,
                    api_key=api_key,
                    model_name=model_name,
                    top_p=top_p,
                )

            if "error" in result:
                assistant_reply = result["error"]
            else:
                assistant_reply = (
                    result.get("choices", [{}])[0].get("message", {}).get("content", "")
                )
            emit("assistant_reply", {"content": assistant_reply})
        except Exception as e:
            print("❌ Error in handle_user_message:", str(e))
            emit("assistant_reply", {"content": f"[Error: {str(e)}]"})
            emit("audio_complete")
