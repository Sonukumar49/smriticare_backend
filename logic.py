from flask import Blueprint, request
from config import get_db
import datetime
from bson import ObjectId

sonu_bp = Blueprint("sonu", __name__)


SAFE_LAT = 12.97
SAFE_LNG = 77.59


# =========================
# SAFE ZONE
# =========================

@sonu_bp.route("/logic/check_zone", methods=["POST"])
def check_zone():

    data = request.json

    lat = data["lat"]
    lng = data["lng"]

    inside = abs(lat - SAFE_LAT) < 0.05 and abs(lng - SAFE_LNG) < 0.05

    return {"inside_safe_zone": inside}


# =========================
# REMINDER
# =========================

@sonu_bp.route("/logic/reminder", methods=["POST"])
def reminder():

    db = get_db()

    data = request.json

    reminder = {
        "patient_id": data["patient_id"],
        "text": data["text"],
        "time": data["time"],
        "status": "pending",
        "created_at": datetime.datetime.utcnow()
    }

    r = db.reminders.insert_one(reminder)

    return {
        "reminder_id": str(r.inserted_id)
    }


@sonu_bp.route("/logic/reminder/<patient_id>")
def get_reminder(patient_id):

    db = get_db()

    data = list(
        db.reminders.find({"patient_id": patient_id})
    )

    for d in data:
        d["_id"] = str(d["_id"])

    return {"reminders": data}


# =========================
# ALERT
# =========================

@sonu_bp.route("/logic/alert", methods=["POST"])
def alert():

    db = get_db()

    data = request.json

    alert = {
        "patient_id": data["patient_id"],
        "type": data["type"],
        "status": "active",
        "time": datetime.datetime.utcnow()
    }

    r = db.alerts.insert_one(alert)

    return {"alert_id": str(r.inserted_id)}


# =========================
# LOCATION
# =========================

@sonu_bp.route("/logic/location", methods=["POST"])
def location():

    db = get_db()

    data = request.json

    loc = {
        "patient_id": data["patient_id"],
        "lat": data["lat"],
        "lng": data["lng"],
        "time": datetime.datetime.utcnow()
    }

    db.location.insert_one(loc)

    return {"status": "saved"}


@sonu_bp.route("/logic/location/<patient_id>")
def location_history(patient_id):

    db = get_db()

    l = list(
        db.location.find({"patient_id": patient_id})
    )

    for x in l:
        x["_id"] = str(x["_id"])

    return {"history": l}


# =========================
# GAME
# =========================

@sonu_bp.route("/logic/game/next")
def game():

    return {
        "question": "Who is this?",
        "options": ["son", "daughter", "doctor"],
        "answer": "son"
    }


@sonu_bp.route("/logic/game/submit", methods=["POST"])
def submit():

    data = request.json

    return {
        "correct": data["answer"] == "son"
    }


# =========================
# REALTIME
# =========================

@sonu_bp.route("/logic/realtime/<patient_id>")
def realtime(patient_id):

    db = get_db()

    alert = db.alerts.find_one({"patient_id": patient_id})
    reminder = db.reminders.find_one({"patient_id": patient_id})

    return {
        "alert": str(alert["_id"]) if alert else None,
        "reminder": str(reminder["_id"]) if reminder else None
    }