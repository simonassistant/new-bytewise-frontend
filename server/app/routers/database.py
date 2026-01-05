import os
import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime

database = Blueprint("database", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

@database.route("/users", methods=["POST"])
def create_or_get_user():
    data = request.get_json()
    username = data.get("username")
    role = data.get("role", "student")
    
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, username, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user:
            return jsonify({"id": user[0], "username": user[1], "role": user[2]})
        
        cur.execute(
            "INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id, username, role",
            (username, role)
        )
        user = cur.fetchone()
        conn.commit()
        return jsonify({"id": user[0], "username": user[1], "role": user[2]}), 201
    finally:
        cur.close()
        conn.close()

@database.route("/sessions", methods=["POST"])
def create_session():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title", "New Chat")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO chat_sessions (user_id, title) VALUES (%s, %s) RETURNING id, title, created_at",
            (user_id, title)
        )
        session = cur.fetchone()
        conn.commit()
        return jsonify({
            "id": session[0],
            "title": session[1],
            "created_at": session[2].isoformat() if session[2] else None
        }), 201
    finally:
        cur.close()
        conn.close()

@database.route("/sessions/<int:user_id>", methods=["GET"])
def get_user_sessions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """SELECT id, title, created_at, updated_at 
               FROM chat_sessions 
               WHERE user_id = %s 
               ORDER BY updated_at DESC""",
            (user_id,)
        )
        sessions = cur.fetchall()
        return jsonify([{
            "id": s[0],
            "title": s[1],
            "created_at": s[2].isoformat() if s[2] else None,
            "updated_at": s[3].isoformat() if s[3] else None
        } for s in sessions])
    finally:
        cur.close()
        conn.close()

@database.route("/messages", methods=["POST"])
def save_message():
    data = request.get_json()
    session_id = data.get("session_id")
    role = data.get("role")
    content = data.get("content")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s) RETURNING id",
            (session_id, role, content)
        )
        msg_id = cur.fetchone()[0]
        cur.execute(
            "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (session_id,)
        )
        conn.commit()
        return jsonify({"id": msg_id}), 201
    finally:
        cur.close()
        conn.close()

@database.route("/messages/<int:session_id>", methods=["GET"])
def get_session_messages(session_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """SELECT id, role, content, created_at 
               FROM messages 
               WHERE session_id = %s 
               ORDER BY created_at ASC""",
            (session_id,)
        )
        messages = cur.fetchall()
        return jsonify([{
            "id": m[0],
            "role": m[1],
            "content": m[2],
            "created_at": m[3].isoformat() if m[3] else None
        } for m in messages])
    finally:
        cur.close()
        conn.close()

@database.route("/students", methods=["GET"])
def get_all_students():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """SELECT u.id, u.username, COUNT(cs.id) as session_count
               FROM users u
               LEFT JOIN chat_sessions cs ON u.id = cs.user_id
               WHERE u.role = 'student'
               GROUP BY u.id, u.username
               ORDER BY u.username"""
        )
        students = cur.fetchall()
        return jsonify([{
            "id": s[0],
            "username": s[1],
            "session_count": s[2]
        } for s in students])
    finally:
        cur.close()
        conn.close()

@database.route("/comments", methods=["POST"])
def add_teacher_comment():
    data = request.get_json()
    session_id = data.get("session_id")
    teacher_id = data.get("teacher_id")
    comment = data.get("comment")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO teacher_comments (session_id, teacher_id, comment) VALUES (%s, %s, %s) RETURNING id, created_at",
            (session_id, teacher_id, comment)
        )
        result = cur.fetchone()
        conn.commit()
        return jsonify({"id": result[0], "created_at": result[1].isoformat() if result[1] else None}), 201
    finally:
        cur.close()
        conn.close()

@database.route("/comments/<int:session_id>", methods=["GET"])
def get_session_comments(session_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """SELECT tc.id, tc.comment, tc.created_at, u.username as teacher_name
               FROM teacher_comments tc
               JOIN users u ON tc.teacher_id = u.id
               WHERE tc.session_id = %s
               ORDER BY tc.created_at DESC""",
            (session_id,)
        )
        comments = cur.fetchall()
        return jsonify([{
            "id": c[0],
            "comment": c[1],
            "created_at": c[2].isoformat() if c[2] else None,
            "teacher_name": c[3]
        } for c in comments])
    finally:
        cur.close()
        conn.close()
