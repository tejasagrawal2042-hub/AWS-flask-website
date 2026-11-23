import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["mydatabase"]
collection = db["users"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Flask backend running"}), 200


@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided."}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return jsonify({
            "error": "Both Name and Email are required."
        }), 400

    try:
        collection.insert_one({
            "name": name,
            "email": email
        })

        return jsonify({
            "message": "Data submitted successfully"
        }), 201

    except PyMongoError:
        app.logger.exception("Database error")

        return jsonify({
            "error": "Database operation failed"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
