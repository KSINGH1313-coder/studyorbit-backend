from flask import Blueprint, request, jsonify
from config.db import db

assignment = Blueprint("assignment", __name__)

# 👉 Create assignment (teacher)
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@assignment.route("/create", methods=["POST"])
def create_assignment():
    title = request.form.get("title")
    description = request.form.get("description")
    deadline = request.form.get("deadline")
    batch_id = request.form.get("batch_id")

    file = request.files.get("file")

    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    db.assignments.insert_one({
        "batch_id": batch_id,
        "title": title,
        "description": description,
        "deadline": deadline,
        "file": filename  # 🔥 optional
    })

    return jsonify({"message": "Assignment created"})


# 👉 Get assignments
@assignment.route("/<batch_id>", methods=["GET"])
def get_assignments(batch_id):
    data = list(db.assignments.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ))
    return jsonify(data)


# 👉 Submit assignment (student)
@assignment.route("/submit", methods=["POST"])
def submit():
    data = request.form

    file = request.files.get("file")

    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join("uploads", filename))

    db.submissions.insert_one({
        "batch_id": data.get("batch_id"),
        "assignment_title": data.get("assignment_title"),
        "student_email": data.get("student_email"),
        "answer": data.get("answer"),
        "file": filename
    })

    return jsonify({"message": "Submitted successfully"})


@assignment.route("/submissions/<batch_id>/<title>", methods=["GET"])
def get_submissions(batch_id, title):
    data = list(db.submissions.find(
        {
            "batch_id": batch_id,
            "assignment_title": title
        },
        {"_id": 0}
    ))

    return jsonify(data)