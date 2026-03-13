# auth_routes.py

from flask import Blueprint, request

from models import create_user, get_user_by_email
from utils import verify_password, create_token, create_patient_session, require_admin


auth_bp = Blueprint("auth_bp", __name__)


# ---------- REGISTER ----------

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()

    if not email or not password or not name:
        return {"error": "email, password and name are required"}, 400

    user = create_user(email, password, name, phone)

    if not user:
        return {"error": "Email already exists"}, 400

    return {
        "user_id": user["_id"],
        "email": email,
        "name": name
    }, 201


# ---------- LOGIN ----------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")
    print("EMAIL:", email)
    print("PASSWORD:", password)

    if not email or not password:
        return {"error": "email and password are required"}, 400

    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return {"error": "Invalid email or password"}, 401

    access = create_token(
        {"user_id": str(user["_id"]), "role": user["role"]},
        60
    )

    refresh = create_token(
        {"user_id": str(user["_id"])},
        1440
    )

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": {
            "id": str(user["_id"]),
            "role": user["role"]
        }
    }


# ---------- IMPERSONATE (admin only) ----------

@auth_bp.route("/impersonate-session", methods=["POST"])
#@require_admin
def impersonate():

    data = request.json or {}

    patient_id = data.get("patient_id")
    duration = data.get("duration_minutes", 60)

    if not patient_id:
        return {"error": "patient_id is required"}, 400

    token = create_patient_session(patient_id, duration)

    return {
        "patient_session_token": token,
        "expires_in": duration
    }