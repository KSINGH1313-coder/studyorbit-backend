from flask import Blueprint, request, jsonify
from config.db import db
from datetime import datetime

test = Blueprint("test", __name__)

# =========================
# ONLINE TEST
# =========================

@test.route("/online/create", methods=["POST"])
def create_online_test():
    data = request.json

    db.tests.insert_one({
        "batch_id": data["batch_id"],
        "title": data["title"],
        "duration": data["duration"],
        "questions": data["questions"]
    })

    return jsonify({"message": "Test created"})


@test.route("/online/<batch_id>", methods=["GET"])
def get_online_tests(batch_id):
    data = list(db.tests.find({"batch_id": batch_id}, {"_id": 0}))
    return jsonify(data)


@test.route("/online/submit", methods=["POST"])
def submit_test():
    data = request.json

    score = 0

    for q, ans in zip(data["questions"], data["answers"]):
        if q["correct"] == ans:
            score += 1

    total = len(data["questions"])
    percentage = (score / total) * 100 if total else 0

    db.online_results.insert_one({
        "batch_id": data["batch_id"],
        "student_email": data["student_email"],
        "title": data["title"],
        "score": score,
        "total": total,
        "percentage": percentage,
        "time": datetime.now().strftime("%H:%M")
    })

    return jsonify({"score": score, "total": total, "percentage": percentage})


@test.route("/online/results/<batch_id>/<email>", methods=["GET"])
def get_results(batch_id, email):
    data = list(db.online_results.find(
        {"batch_id": batch_id, "student_email": email},
        {"_id": 0}
    ))
    return jsonify(data)


# 🔥 NEW → ALL RESULTS FOR TEACHER
@test.route("/online/all-results/<batch_id>", methods=["GET"])
def get_all_results(batch_id):
    data = list(db.online_results.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ).sort("percentage", -1))

    return jsonify(data)

@test.route("/offline/<batch_id>", methods=["GET"])
def get_offline_tests(batch_id):
    data = list(db.offline_tests.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ))
    return jsonify(data)

@test.route("/offline/create", methods=["POST"])
def create_offline_test():
    data = request.json

    db.offline_tests.insert_one({
        "batch_id": data["batch_id"],
        "title": data["title"],
        "date": data["date"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "max_marks": data["max_marks"]
    })

    return jsonify({"message": "Offline test scheduled successfully"})

@test.route("/offline/results/<batch_id>/<email>", methods=["GET"])
def get_offline_results(batch_id, email):
    data = list(db.offline_results.find(
        {
            "batch_id": batch_id,
            "student_email": email
        },
        {"_id": 0}
    ))

    return jsonify(data)

@test.route("/offline/leaderboard/<batch_id>", methods=["GET"])
def get_leaderboard(batch_id):
    data = list(db.offline_results.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ).sort("percentage", -1))

    return jsonify(data)

@test.route("/offline/result/upload", methods=["POST", "OPTIONS"])
def upload_offline_result():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    try:
        marks = float(data["marks"])
        total = float(data["total"])

        # 🔥 FIX: prevent division by zero
        if total == 0:
            return jsonify({"error": "Total marks cannot be 0"}), 400

        percentage = (marks / total) * 100

        db.offline_results.insert_one({
            "batch_id": str(data["batch_id"]),
            "test_title": data["test_title"],
            "student_email": data["student_email"],
            "marks": marks,
            "total": total,
            "percentage": percentage
        })

        return jsonify({"message": "Uploaded successfully"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"}), 500