from flask import Blueprint, request, jsonify
from config.db import db
from bson import ObjectId

batch = Blueprint("batch", __name__)

# =====================================================
# 👉 CREATE BATCH
# =====================================================
@batch.route("/create", methods=["POST"])
def create_batch():
    data = request.json

    if not data.get("name") or not data.get("teacher_email"):
        return jsonify({"message": "Missing required fields"}), 400

    result = db.batches.insert_one({
        "name": data["name"],
        "teacher_email": data["teacher_email"],
        "students": []
    })

    return jsonify({
        "message": "Batch created",
        "batch_id": str(result.inserted_id)
    }), 201


# =====================================================
# 👉 GET TEACHER BATCHES
# =====================================================
@batch.route("/teacher/<email>", methods=["GET"])
def get_batches(email):
    batches = list(db.batches.find({"teacher_email": email}))

    for b in batches:
        b["_id"] = str(b["_id"])

    return jsonify(batches), 200


# =====================================================
# 👉 GET STUDENTS (by institute code)
# =====================================================
@batch.route("/students/<code>", methods=["GET"])
def get_students(code):
    students = list(
        db.users.find(
            {"role": "student", "institute_code": code},
            {"_id": 0, "password": 0}
        )
    )

    return jsonify(students), 200


# =====================================================
# 👉 ADD STUDENT TO BATCH (FINAL FIXED)
# =====================================================
@batch.route("/add-student", methods=["POST"])
def add_student():
    data = request.json

    batch_id = data.get("batch_id")
    student_email = data.get("student_email")

    if not batch_id or not student_email:
        return jsonify({"message": "Missing required fields"}), 400

    try:
        result = db.batches.update_one(
            {"_id": ObjectId(batch_id)},
            {"$addToSet": {"students": student_email}}
        )

        if result.matched_count == 0:
            return jsonify({"message": "Batch not found"}), 404

        if result.modified_count == 0:
            return jsonify({"message": "Student already added"}), 200

        return jsonify({"message": "Student added successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# =====================================================
# 👉 GET STUDENT BATCHES
# =====================================================
@batch.route("/student/<email>", methods=["GET"])
def get_student_batches(email):
    batches = list(db.batches.find({"students": email}))

    result = []

    for b in batches:
        result.append({
            "_id": str(b["_id"]),   # 🔥 VERY IMPORTANT
            "name": b["name"]
        })

    return jsonify(result), 200