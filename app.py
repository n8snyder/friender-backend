import os
import dotenv
import werkzeug
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError

from schemas import signup_schema, login_schema
from models import db, connect_db, User, Picture
from middleware import auth_token

dotenv.load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

CORS(app)

connect_db(app)


@app.route("/signup", methods=["POST"])
@expects_json(signup_schema)
def signup():
    """Handle user signup.

    Create new user and add to DB.

    Return error if email already taken.
    """
    try:
        user = User.register(**g.data)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return (jsonify({"error": "email already taken"}), 400)

    token = user.create_token()
    return (jsonify({"token": token}), 201)
    return jsonify({"success": True})


@app.route("/login", methods=["POST"])
@expects_json(login_schema)
def login():
    """Handle user login."""

    user = User.authenticate(**g.data)

    if user:
        token = user.create_token()
        return (jsonify({"token": token}), 200)

    return (jsonify({"error": "Invalid email/password"}), 400)


@app.route("/users/<int:user_id>")
@auth_token()
def get_user(user_id):
    """Get info about user"""

    user = User.query.get_or_404(user_id)
    return jsonify(user=user.serialize())


@app.route("/users")
@auth_token()
def get_users():
    """Get users in your area"""

    radius = request.args.get("radius")
    zip_code = request.args.get("zip_code")
    num_users = request.args.get("num_users", 10)

    users = User.get_nearby(radius, zip_code, num_users)
    serializedUsers = [
        {
            "id": user.id,
            "name": user.name,
            "hobbies": user.hobbies,
            "interests": user.interests,
            "pictures": [picture.serialize() for picture in user.pictures],
        }
        for user in users
    ]
    print("THESE ARE THE NEARBY USERS:", serializedUsers)
    return (jsonify({"users": serializedUsers}), 200)


@app.route("/pictures", methods=["POST"])
@auth_token()
def create_picture():
    """Handle picture upload and save to db"""

    req_picture = request.files.get("picture")
    if req_picture:
        picture = Picture.create(picture=req_picture, user_id=g.user_id)
        return (jsonify(picture=picture.serialize()), 201)
    raise werkzeug.exceptions.BadRequest('Missing file "picture"')


@app.route("/pictures/<int:pic_id>", methods=["DELETE"])
@auth_token()
def delete_picture(pic_id):
    """Handle picture deletion from s3 and db"""

    picture = Picture.query.get_or_404(pic_id)
    if picture.user_id != g.user_id:
        # Prevent deleting another user's picture
        raise werkzeug.exceptions.Unauthorized()

    picture.delete()
    return jsonify({"success": True})


@app.route("/users/<int:user_id>/pictures", methods=["GET"])
def get_pictures(user_id):
    """Get all pictures belonging to a user"""

    user = User.query.get_or_404(user_id)
    pictures = user.pictures
    return (
        jsonify(pictures=[picture.serialize() for picture in pictures]),
        200,
    )


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return (jsonify({"error": e.description.message}), 400)


@app.errorhandler(werkzeug.exceptions.Unauthorized)
def handle_bad_request(e):
    return (jsonify({}), 401)
