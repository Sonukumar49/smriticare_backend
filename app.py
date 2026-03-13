from flask import Flask
from flask_cors import CORS   # ADD THIS
from config import init_db

from auth_routes import auth_bp
from patient_routes import patient_bp
from extra_routes import extra_bp
from logic import sonu_bp


app = Flask(__name__)

CORS(app)   # ADD THIS LINE

db = init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(patient_bp, url_prefix="/patients")
app.register_blueprint(extra_bp)
app.register_blueprint(sonu_bp)


@app.route("/")
def home():
    return {"msg": "running"}


if __name__ == "__main__":
    app.run(debug=True, port=3000)