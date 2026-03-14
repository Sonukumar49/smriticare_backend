# utils.py

import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import JWT_SECRET, PATIENT_SESSION_SECRET


# ---------------- PASSWORD ----------------

def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, hashed):
    return check_password_hash(hashed, password)


# ---------------- JWT ----------------

def create_token(data, minutes=14400):

    payload = {
        "data": data,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token


def verify_token(token):

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["data"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# -------- patient session token --------

def create_patient_session(patient_id, minutes):

    payload = {
        "patient_id": str(patient_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    }

    token = jwt.encode(
        payload,
        PATIENT_SESSION_SECRET,
        algorithm="HS256"
    )

    return token


def verify_patient_session(token):

    try:
        payload = jwt.decode(token, PATIENT_SESSION_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ---------------- AUTH DECORATOR ----------------

from functools import wraps
from flask import request


def require_auth(f):
    """Decorator that validates Bearer JWT on protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header"}, 401

        token = auth_header.split(" ", 1)[1]
        data = verify_token(token)

        if not data:
            return {"error": "Token invalid or expired"}, 401

        request.current_user = data
        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    """Decorator that validates Bearer JWT and checks for admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header"}, 401

        token = auth_header.split(" ", 1)[1]
        data = verify_token(token)

        if not data:
            return {"error": "Token invalid or expired"}, 401

        if data.get("role") != "admin":
            return {"error": "Forbidden: admin role required"}, 403

        request.current_user = data
        return f(*args, **kwargs)

    return decorated