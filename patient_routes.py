# patient_routes.py

from flask import Blueprint, request
from models import create_patient, get_patient
from config import get_db
from utils import require_auth

patient_bp = Blueprint("patients", __name__)


# ---------- CREATE PATIENT ----------

@patient_bp.route("", methods=["POST"])
@require_auth
def add_patient():

    data = request.json or {}

    if not data.get("display_name"):
        return {"error": "display_name is required"}, 400

    patient = {
        "display_name": data.get("display_name"),
        "birth_year": data.get("birth_year"),
        "gender": data.get("gender"),
        "primary_caregiver_id": data.get("primary_caregiver_id"),
        "timezone": data.get("timezone")
    }

    result = create_patient(patient)

    return {
        "patient_id": result["_id"],
        "display_name": result["display_name"]
    }, 201


# ---------- GET PATIENT ----------

@patient_bp.route("/<patient_id>", methods=["GET"])
@require_auth
def get_one(patient_id):

    patient = get_patient(patient_id)

    if not patient:
        return {"error": "Patient not found"}, 404

    patient["_id"] = str(patient["_id"])

    return {"patient": patient}


# ---------- PERSONA ----------

@patient_bp.route("/<patient_id>/persona", methods=["PUT"])
@require_auth
def update_persona(patient_id):

    data = request.json or {}

    db = get_db()

    db.persona.update_one(
        {"patient_id": patient_id},
        {
            "$set": {
                "greeting_script": data.get("greeting_script"),
                "tts_voice": data.get("tts_voice"),
                "avatar_image_url": data.get("avatar_image_url")
            }
        },
        upsert=True
    )

    return {"status": "updated"}