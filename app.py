import os
import dotenv
import werkzeug
from flask import Flask, jsonify, g
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from schemas import signup_schema, login_schema

dotenv.load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

connect_db(app)


@app.route("/signup", methods=["POST"])
@expects_json(signup_schema)
def signup():
    """Handle user signup.

    Create new user and add to DB.

    Return error if username
    """
    try:
        user = User.register(**g.data)
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        return (jsonify({"error": "email already taken"}), 400)

    token = user.create_token()
    return (jsonify({"token": token}), 201)


@app.route("/login", methods=["POST"])
@expects_json(login_schema)
def login():
    """Handle user login."""

    user = User.authenticate(**g.data)

    if user:
        token = user.create_token()
        return (jsonify({"token": token}), 200)

    return (jsonify({"error": "Invalid email/password"}), 400)


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return (jsonify({"error": e.description.message}), 400)
