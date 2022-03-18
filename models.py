import boto3
import jwt
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql.expression import func
from uuid import uuid4

load_dotenv()

bcrypt = Bcrypt()
db = SQLAlchemy()


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)
BUCKET_NAME = os.environ["BUCKET_NAME"]


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

    zip_code = db.Column(
        db.Text,
        nullable=False,
    )

    radius = db.Column(
        db.Integer,
        nullable=False,
    )

    pictures = db.relationship("Picture")

    @classmethod
    def register(
        cls,
        email,
        password,
        name,
        zip_code,
        hobbies="",
        interests="",
        radius=5,
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
            radius=radius,
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

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "hobbies": self.hobbies,
            "interests": self.interests,
            "zip_code": self.zip_code,
            "radius": self.radius,
        }

    @classmethod
    def get_nearby(cls, radius, zip_code, num_users):
        """Get users that are within the radius from the zip code"""
        # TODO: figure out how to get nearby
        # TODO: exclude disliked users, yourself

        return cls.query.order_by(func.random()).limit(num_users)


class Picture(db.Model):
    """Picture"""

    __tablename__ = "pictures"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    filename = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    @property
    def url(self):
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{self.filename}"

    @classmethod
    def create(cls, picture, user_id):
        file_extention = os.path.splitext(picture.filename)[1]
        filename = f"{uuid4()}{file_extention}"
        picture.filename = filename
        s3.upload_fileobj(Bucket=BUCKET_NAME, Fileobj=picture, Key=filename)
        picture = Picture(filename=filename, user_id=user_id)
        db.session.add(picture)
        db.session.commit()
        return picture

    def delete(self):
        s3.delete_object(Bucket=BUCKET_NAME, Key=self.filename)
        db.session.delete(self)
        return db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
        }


def connect_db(app):
    db.app = app
    db.init_app(app)
