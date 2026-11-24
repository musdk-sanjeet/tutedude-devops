from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)

db = client["Tudedude"]
collection = db["students"]


# TASK 1: GET STUDENT DATA
@app.route("/api", methods=["GET"])
def api():

    data = list(collection.find({}))

    for student in data:
        student["_id"] = str(student["_id"])

    return jsonify(data)


# TASK 2: INSERT STUDENT DATA
@app.route("/students", methods=["POST"])
def add_student():

    student = request.get_json()

    name = student.get("name", "").strip()
    email = student.get("email", "").strip()
    course = student.get("course", "").strip()

    if not name or not email or not course:
        return jsonify({
            "error": "All fields are required!"
        }), 400

    student_data = {
        "name": name,
        "email": email,
        "course": course
    }

    result = collection.insert_one(student_data)

    return jsonify({
        "message": "Student added successfully!",
        "inserted_id": str(result.inserted_id)
    }), 201

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    itemName = request.form.get('itemName')
    itemDescription = request.form.get('itemDescription')

    todo = {
        "itemName": itemName,
        "itemDescription": itemDescription
    }

    collection.insert_one(todo)

    return jsonify({
        "message": "Todo item saved successfully"
    })


if __name__ == "__main__":
    app.run(port=9000, debug=True)
