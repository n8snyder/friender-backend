"""Seed database with sample data from CSV Files."""

from sqlalchemy.sql.expression import func

from csv import DictReader
from app import db
from models import User

db.drop_all()
db.create_all()

# with open("generator/users.csv") as users:
#     db.session.bulk_insert_mappings(User, DictReader(users))

# with open("generator/messages.csv") as messages:
#     db.session.bulk_insert_mappings(Message, DictReader(messages))

# with open("generator/follows.csv") as follows:
#     db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()


user = User(
    email="test@test.com",
    password="$2b$12$lkFyBkmiDof8Tqt/dv1G9ey5aNV297Ed8l6z3zGmJwujeiiEgFhUq",
    name="Testy Testerson",
    hobbies="None",
    interests="A few",
    zip_code="94709",
    radius=5,
)

db.session.add(user)
db.session.commit()

# followers = User.query.order_by(func.random()).limit(10).all()
# following = User.query.order_by(func.random()).limit(10).all()
# user.followers += followers
# user.following += following
# db.session.commit()
