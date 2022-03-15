""" Schemas for API requests"""

signup_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "name": {"type": "string"},
        "zip_code": {"type": "string"},
        "hobbies": {"type": "string"},
        "interests": {"type": "string"},
        "friend_radius": {"type": "number"},
    },
    "required": ["email", "password", "name", "zip_code"],
}

login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
}
