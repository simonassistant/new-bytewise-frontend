import requests
from flask import Blueprint, jsonify, request

# ------------------------------
# Blueprint (REST endpoint)
# ------------------------------
openrouter = Blueprint("openrouter", __name__)


@openrouter.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module openrouter"})


