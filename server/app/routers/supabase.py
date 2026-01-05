import requests, os
from supabase import create_client, Client
from flask import Blueprint, jsonify, request

# ------------------------------
# Blueprint (REST endpoint)
# ------------------------------
supabase = Blueprint("supabase", __name__)


@supabase.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module supabase"})


@supabase.route("/add_comment", methods=["POST"])
def add_comment():
    """
    Receives JSON data:
    Inserts it into the student_comments table.
    """

    data = request.get_json()
    if not data or "rating" not in data or "comment" not in data:
        return jsonify({"error": "Missing 'rating' or 'comment'"}), 400

    rating = data.get("rating")
    comment = data.get("comment")

    try:
        SUPABASE_URL = "http://8.211.158.223:8000"
        SUPABASE_KEY = os.getenv(
            "SUPABASE_KEY"
        )  # Always safer to keep keys in env vars

        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        # Insert into Supabase table
        response = (
            supabase.table("student_comments")
            .insert({"rating": rating, "comment": comment})
            .execute()
        )

        if response.data:
            return (
                jsonify(
                    {"message": "Comment added successfully", "data": response.data}
                ),
                201,
            )
        else:
            return (
                jsonify({"error": "Failed to insert data", "details": response.error}),
                400,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
