from flask import Blueprint, request, jsonify
from config.db import db
import random
import string

auth = Blueprint("auth", __name__)

# 🔥 generate institute code
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# 👉 Teacher Signup
@auth.route("/teacher/signup", methods=["POST"])
def teacher_signup():
    data = request.json

    import random, string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    teacher = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "role": "teacher",
        "institute_code": code
    }

    db.users.insert_one(teacher)

    return jsonify({
        "message": "Teacher registered",
        "institute_code": code
    })

# 👉 Student Signup
@auth.route("/student/signup", methods=["POST"])
def student_signup():
    data = request.json

    student = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "role": "student",
        "institute_code": data["instituteCode"]  # 🔥 important
    }

    db.users.insert_one(student)

    return jsonify({"message": "Student registered"})
   

# 👉 Login (common for both)
@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    user = db.users.find_one({
        "email": data["email"],
        "password": data["password"]
    })

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "institute_code": user["institute_code"]
        }
    })