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
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data received"}), 400

        # ✅ safe extraction
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"message": "Missing fields"}), 400

        code = generate_code()

        teacher = {
            "name": name,
            "email": email,
            "password": password,
            "role": "teacher",
            "institute_code": code
        }

        db.users.insert_one(teacher)

        return jsonify({
            "message": "Teacher registered",
            "institute_code": code
        })

    except Exception as e:
        print("ERROR:", e)  # 🔥 important for logs
        return jsonify({"message": "Server error"}), 500


# 👉 Student Signup
@auth.route("/student/signup", methods=["POST"])
def student_signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data received"}), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        institute_code = data.get("instituteCode")

        if not name or not email or not password or not institute_code:
            return jsonify({"message": "Missing fields"}), 400

        student = {
            "name": name,
            "email": email,
            "password": password,
            "role": "student",
            "institute_code": institute_code
        }

        db.users.insert_one(student)

        return jsonify({"message": "Student registered"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# 👉 Login
@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data received"}), 400

        user = db.users.find_one({
            "email": data.get("email"),
            "password": data.get("password")
        })

        if not user:
            return jsonify({"message": "Invalid credentials"}), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "institute_code": user.get("institute_code", "")
            }
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Server error"}), 500