login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['email', 'password']
}

sign_up_schema = {
    "title": "User Signup Form Schema",
    "description": "A JSON schema for validating user signup form data.",
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "description": "The user's first name.",
            "pattern": "^[a-zA-ZçÇğĞıİöÖşŞüÜ]+$",
            "maxLength": 50
        },
        "last_name": {
            "type": "string",
            "description": "The user's last name.",
            "pattern": "^[a-zA-ZçÇğĞıİöÖşŞüÜ]+$",
            "maxLength": 50
        },
        "email": {
            "type": "string",
            "description": "The user's email address.",
            "maxLength": 255,
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "password": {
            "type": "string",
            "description": "The user's password.",
            "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$",
            "maxLength": 100
        }
    },
    "required": ["first_name", "last_name", "email", "password"]
}
