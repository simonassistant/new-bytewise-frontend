import os
import secrets
import requests
from flask import Flask, request, redirect, jsonify, session, make_response
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', secrets.token_hex(32))
FRONTEND_ORIGIN = os.environ.get('FRONTEND_ORIGIN', 'http://localhost:5000')
CORS(app, supports_credentials=True, origins=[FRONTEND_ORIGIN])

AUTH_SERVER = "https://auth.hkbu.tech"
CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET', '')
REDIRECT_URI = os.environ.get('OAUTH_REDIRECT_URI', '')

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/auth/login')
def login():
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    auth_url = f"{AUTH_SERVER}/auth-provider/login"
    params = f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}"
    
    return jsonify({"auth_url": auth_url + params})

@app.route('/api/auth/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code:
        return redirect('/?error=no_code')
    
    expected_state = session.get('oauth_state')
    if state != expected_state:
        return redirect('/?error=invalid_state')
    
    try:
        token_response = requests.post(
            f"{AUTH_SERVER}/api/oauth/token",
            json={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI
            },
            headers={"Content-Type": "application/json"}
        )
        
        if token_response.status_code != 200:
            return redirect('/?error=token_exchange_failed')
        
        token_data = token_response.json()
        session['access_token'] = token_data.get('access_token')
        session['token_type'] = token_data.get('token_type', 'Bearer')
        
        return redirect('/')
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect('/?error=oauth_error')

@app.route('/api/auth/status')
def auth_status():
    access_token = session.get('access_token')
    if access_token:
        return jsonify({"authenticated": True})
    return jsonify({"authenticated": False})

@app.route('/api/auth/logout')
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/chat', methods=['POST'])
def chat():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    chat_history = data.get('chat_history', [])
    model = data.get('model', 'gpt-4.1-mini')
    
    return jsonify({
        "error": "Platform AI endpoint not configured. Please provide the API endpoint URL."
    }), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
