from services.auth import AuthService
from functools import wraps
from flask import request, jsonify
from utils.functions import decode_token
from create_app.redis import redis_conn


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
                current_user = {
                    'user_id': payload['user_id'],
                    'session_key': payload['session_key'],
                    'role': payload['role']
                }

                if redis_conn.exists(current_user["user_id"]):
                    return jsonify({'message': 'User is banned.'}), 403

                if current_user['role'] not in roles:
                    return jsonify(message='Unauthorized'), 401
            except Exception as ex:
                return jsonify(message=f"{ex}"), 400

            return f(current_user, *args, **kwargs)

        return decorated_function
    return decorator




