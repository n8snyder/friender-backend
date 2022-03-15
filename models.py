import jwt
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    hobbies = db.Column(
        db.Text,
    )

    interests = db.Column(
        db.Text,
    )

    # zip code
    zip_code = db.Column(
        db.Text,
        nullable=False,
    )

    friend_radius = db.Column(
        db.Integer,
        nullable=False,
    )

    @classmethod
    def register(
        cls,
        email,
        password,
        name,
        zip_code,
        hobbies="",
        interests="",
        friend_radius=5,
    ):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode("utf8")

        # return instance of user w/email and hashed password
        return cls(
            email=email,
            password=hashed,
            name=name,
            hobbies=hobbies,
            interests=interests,
            zip_code=zip_code,
            friend_radius=friend_radius,
        )

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(email=email).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    def create_token(self):
        """Return a signed JWT with payload { user_id }"""

        return jwt.encode(
            {"user_id": self.id}, os.environ["SECRET_KEY"], algorithm="HS256"
        )


def connect_db(app):
    db.app = app
    db.init_app(app)
