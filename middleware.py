import jwt
import os
from flask import request, g
from functools import wraps
from werkzeug.exceptions import Unauthorized


def auth_token():
    """Authenticate token and store user_id in g"""

    def _auth_token(func):
        @wraps(func)
        def __auth_token(*args, **kwargs):
            token = (
                request.headers.get("Authorization", "")
                .replace("Bearer ", "")
                .strip()
            )
            try:
                payload = jwt.decode(
                    token, os.environ["SECRET_KEY"], algorithms=["HS256"]
                )
            except jwt.exceptions.DecodeError:
                raise Unauthorized()
            g.user_id = payload.get("user_id")

            return func(*args, **kwargs)

        return __auth_token

    return _auth_token
