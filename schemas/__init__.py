from functools import wraps
from jsonschema import validate, ValidationError
from flask import request, jsonify


def validate_json(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Take the JSON data and validate it
            data = request.get_json()

            # If the validation fails, return a 400 Bad Request response
            try:
                validate(data, schema)
            except ValidationError as e:
                return jsonify({'error': e.message}), 400

            # Otherwise, proceed with the function call and return the result.
            return func(*args, **kwargs)

        return wrapper
    return decorator
