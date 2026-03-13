# extra_routes.py

from flask import Blueprint, request
from config import get_db
from bson import ObjectId
import datetime

extra_bp = Blueprint("extra", __name__)


# ===============================
# ROUTINES
# ===============================

@extra_bp.route("/patients/<patient_id>/routines", methods=["POST"])
def create_routine(patient_id):

    db = get_db()

    data = request.json

    routine = {
        "patient_id": patient_id,
        "title": data.get("title"),
        "schedule": data.get("schedule"),
        "description": data.get("description"),
        "created_at": datetime.datetime.utcnow()
    }

    r = db.routines.insert_one(routine)

    return {
        "routine_id": str(r.inserted_id),
        "patient_id": patient_id
    }, 201


@extra_bp.route("/patients/<patient_id>/routines", methods=["GET"])
def get_routines(patient_id):

    db = get_db()

    routines = list(db.routines.find({"patient_id": patient_id}))

    for r in routines:
        r["_id"] = str(r["_id"])

    return {"routines": routines}


# ===============================
# REMINDER ACK
# ===============================

@extra_bp.route("/reminders/<reminder_id>/ack", methods=["POST"])
def ack(reminder_id):

    db = get_db()

    db.reminders.update_one(
        {"_id": ObjectId(reminder_id)},
        {
            "$set": {
                "status": "acknowledged",
                "acknowledged_at": datetime.datetime.utcnow()
            }
        }
    )

    return {
        "reminder_id": reminder_id,
        "status": "acknowledged"
    }


# ===============================
# AI INTERACT (fake)
# ===============================

@extra_bp.route("/ai/interact", methods=["POST"])
def ai():

    return {
        "reply_text": "It's time for your medicine",
        "reply_audio_url": "https://audio.fake",
        "avatar_gif_url": "https://avatar.fake",
        "expected_actions": ["ack"]
    }


# ===============================
# LOCATION
# ===============================

@extra_bp.route("/patients/<patient_id>/location", methods=["POST"])
def location(patient_id):

    db = get_db()

    data = request.json

    loc = {
        "patient_id": patient_id,
        "coords": data.get("coords"),
        "accuracy": data.get("accuracy_m"),
        "time": datetime.datetime.utcnow()
    }

    db.location.insert_one(loc)

    return {
        "status": "ok",
        "in_safe_zone": True
    }


@extra_bp.route("/patients/<patient_id>/location/history")
def location_history(patient_id):

    db = get_db()

    locs = list(
        db.location.find({"patient_id": patient_id}).limit(50)
    )

    for l in locs:
        l["_id"] = str(l["_id"])

    return {"history": locs}


# ===============================
# ALERTS
# ===============================

@extra_bp.route("/alerts")
def alerts():

    db = get_db()

    alerts = list(db.alerts.find())

    for a in alerts:
        a["_id"] = str(a["_id"])

    return {"alerts": alerts}


@extra_bp.route("/alerts/<alert_id>/ack", methods=["POST"])
def alert_ack(alert_id):

    db = get_db()

    db.alerts.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {"status": "resolved"}}
    )

    return {"status": "ok"}


# ===============================
# EXERCISE
# ===============================

@extra_bp.route("/patients/<patient_id>/exercise/next")
def exercise(patient_id):

    return {
        "exercise": {
            "slug": "face_match",
            "content": {},
            "timeout": 30
        }
    }


@extra_bp.route(
    "/patients/<patient_id>/exercise/<slug>/submit",
    methods=["POST"]
)
def submit(patient_id, slug):

    return {
        "correct": True,
        "next_suggestion": "good"
    }