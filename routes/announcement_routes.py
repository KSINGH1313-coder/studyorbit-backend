from flask import Blueprint, request, jsonify
from config.db import db

announcement = Blueprint("announcement", __name__)

from datetime import datetime

@announcement.route("/send", methods=["POST"])
def send():
    data = request.json

    db.announcements.insert_one({
        "batch_id": data["batch_id"],
        "message": data["message"],
        "sender": data["sender"],  # teacher / student
        "name": data["name"],      # 🔥 sender name
        "time": datetime.now().strftime("%H:%M")
    })

    return jsonify({"message": "Sent"})


@announcement.route("/<batch_id>", methods=["GET"])
def get(batch_id):
    data = list(db.announcements.find(
        {"batch_id": batch_id},
        {"_id": 0}
    ))
    return jsonify(data)