# config.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "SmritiCare")

JWT_SECRET = os.getenv("JWT_SECRET")
PATIENT_SESSION_SECRET = os.getenv("PATIENT_SESSION_SECRET")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

if not JWT_SECRET or not PATIENT_SESSION_SECRET or not FLASK_SECRET_KEY:
    raise RuntimeError("Missing required secrets in .env: JWT_SECRET, PATIENT_SESSION_SECRET, FLASK_SECRET_KEY")

client = None
db = None


def init_db(app):

    global client
    global db

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    print("Mongo connected")

    return db


def get_db():
    return db