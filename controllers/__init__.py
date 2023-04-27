from services.auth import AuthService
from functools import wraps
from flask import request, jsonify
from utils.functions import decode_token


auth_service = AuthService()


def required_roles(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify(message='Token is missing'), 401

            try:
                payload = decode_token(token)
                user_role = payload['role']
                if user_role not in roles:
                    return jsonify(message='Unauthorized'), 401
            except Exception as ex:
                return jsonify({'error': ex}), 400

            return f(*args, **kwargs)

        return decorated_function
    return decorator
