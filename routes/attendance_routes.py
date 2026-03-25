from flask import Blueprint, request, jsonify
from config.db import db
from datetime import datetime

attendance = Blueprint("attendance", __name__)

# 👉 Mark attendance
@attendance.route("/mark", methods=["POST"])
def mark_attendance():
    data = request.json

    db.attendance.update_one(
        {
            "batch_id": data["batch_id"],
            "student_email": data["student_email"],
            "date": data["date"]
        },
        {
            "$set": {
                "status": data["status"]
            }
        },
        upsert=True  # 🔥 prevents duplicate
    )

    return jsonify({"message": "Attendance saved"})


# 👉 Get attendance (student)
@attendance.route("/student/<batch_id>/<email>", methods=["GET"])
def get_student_attendance(batch_id, email):
    records = list(db.attendance.find({
        "batch_id": batch_id,
        "student_email": email
    }, {"_id": 0}))

    return jsonify(records)