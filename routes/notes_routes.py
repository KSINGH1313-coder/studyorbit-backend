import os
from flask import Blueprint, request, jsonify
from config.db import db

notes = Blueprint("notes", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@notes.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title")
    description = request.form.get("description")
    batch_id = request.form.get("batch_id")

    file = request.files.get("file")

    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    db.notes.insert_one({
        "batch_id": batch_id,   # 🔥 FIX
        "title": title,
        "description": description,
        "file": filename
    })

    return jsonify({"message": "Note added successfully"})


@notes.route("/<batch_id>", methods=["GET"])
def get_notes(batch_id):
    notes_list = list(db.notes.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ))

    return jsonify(notes_list)