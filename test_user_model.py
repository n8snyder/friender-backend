"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User, bcrypt

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ["DATABASE_URL"] = "postgresql:///friender_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        self.client = app.test_client()
        self.password = "FeL7f23#1"
        self.email1 = "foo1@bar.com"
        self.email2 = "foo2@bar.com"
        self.zip_code = "94709"
        self.name1 = "name1"
        self.name2 = "name2"
        user1 = User(
            email=self.email1,
            password=bcrypt.generate_password_hash(self.password).decode(
                "UTF-8",
            ),
            zip_code=self.zip_code,
            name=self.name1,
            radius=5,
        )
        user2 = User(
            email=self.email2,
            password=bcrypt.generate_password_hash(self.password).decode(
                "UTF-8"
            ),
            zip_code=self.zip_code,
            name=self.name2,
            radius=5,
        )
        db.session.add_all([user1, user2])
        db.session.commit()
        self.user1_id = user1.id
        self.user2_id = user2.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        user = User(
            email="unique@email.com",
            password="HASHED_PASSWORD",
            name="Test Name",
            zip_code=self.zip_code,
            radius=5,
        )

        db.session.add(user)
        db.session.commit()

        # User should have no pictures
        self.assertEqual(len(user.pictures), 0)

        self.assertIs(user.hobbies, None)
        self.assertIs(user.interests, None)

    def test_register_works(self):

        user = User.register(
            email="unique@mail.com",
            password="123123",
            name="Test Testerson",
            zip_code="94709",
            hobbies="Debugging code",
            interests="Computers",
            radius=777,
        )

        # Are the attributes correct?
        self.assertEqual(user.email, "unique@mail.com")
        self.assertEqual(user.name, "Test Testerson")
        self.assertEqual(user.zip_code, "94709")
        self.assertEqual(user.hobbies, "Debugging code")
        self.assertEqual(user.interests, "Computers")
        self.assertEqual(user.radius, 777)

        # Is the user in the database before commit?
        self.assertIsNone(user.id)

        db.session.add(user)
        db.session.commit()

        # Is the user in the database after commit?
        self.assertIsNotNone(user.id)

    def test_register_default_values(self):

        user = User.register(
            email="unique@mail.com",
            password="123123",
            name="Test Testerson",
            zip_code="94709",
        )

        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.hobbies, "")
        self.assertEqual(user.interests, "")
        self.assertEqual(user.radius, 5)

    def test_register_fails_uniqueness(self):

        # Does signing up a user with a non-unique email fail?
        user = User.register(
            email=self.email1,
            password="123123",
            name="Test Testerson",
            zip_code="94709",
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            # Correct behavior
            db.session.rollback()
        else:
            self.fail("Exception not raised.")

    def test_register_fails_nullable(self):
        """Does User.register fail when given None for non-nullable fields?"""

        # Does signing up a user with email of None fail?
        user = User.register(
            email=None,
            password="123123",
            name="Test Testerson",
            zip_code="94709",
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            # Correct behavior
            db.session.rollback()
        else:
            self.fail("Exception not raised when email is null.")

        # Does signing up a user with zip_code of None fail?
        user = User.register(
            email="unique@mail.com",
            password="123123",
            name="Test Testerson",
            zip_code=None,
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            # Correct behavior
            db.session.rollback()
        else:
            self.fail("Exception not raised when zip_code is null.")

        # Does signing up a user with name of None fail?
        user = User.register(
            email="unique@mail.com",
            password="123123",
            name=None,
            zip_code=self.zip_code,
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            # Correct behavior
            db.session.rollback()
        else:
            self.fail("Exception not raised when name is null.")

        # Does signing up a user with password of None fail?
        try:
            User.register(
                email="unique@mail.com",
                password=None,
                name="Test Testerson",
                zip_code=self.zip_code,
            )
        except:
            # Correct behavior
            pass
        else:
            self.fail("Exception not raised when password is null.")
