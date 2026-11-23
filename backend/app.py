import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS 
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()
app = Flask(__name__)
CORS(app) 

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["users"]

@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided."}), 400
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return jsonify({"error": "Both Name and Email are required."}), 400
    try:
        collection.insert_one({"name": name, "email": email})
        return jsonify({"message": "Data submitted successfully"}), 201
    except PyMongoError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
