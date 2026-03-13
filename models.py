# models.py

from bson import ObjectId
from bson.errors import InvalidId
from config import get_db
from utils import hash_password


# ---------------- USER ----------------

def create_user(email, password, name, phone):

    db = get_db()

    existing = db.users.find_one({"email": email})

    if existing:
        return None

    user = {
        "email": email,
        "password_hash": hash_password(password),
        "name": name,
        "phone": phone,
        "role": "caregiver"
    }

    result = db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)

    return user


def get_user_by_email(email):

    db = get_db()
    return db.users.find_one({"email": email})


def get_user_by_id(user_id):

    db = get_db()

    try:
        return db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        return None


# ---------------- PATIENT ----------------

def create_patient(data):

    db = get_db()

    result = db.patients.insert_one(data)
    data["_id"] = str(result.inserted_id)

    return data


def get_patient(patient_id):

    db = get_db()

    try:
        return db.patients.find_one({"_id": ObjectId(patient_id)})
    except InvalidId:
        return None