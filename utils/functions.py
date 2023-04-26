import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_mail import Mail, Message
from flask import url_for
from flask import current_app
import base64


load_dotenv()


def is_base64(s):
    try:
        # Attempt to decode the data from base64
        if isinstance(s, str):
            # If the data is a string, convert it to bytes first
            s = bytes(s, 'utf-8')
        # Check if the decoded data can be encoded back to base64
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        # If an exception is thrown during the decoding or encoding process, return False
        return False


def send_verification_email(verify_token, email):
    try:
        with current_app.app_context():
            mail = Mail()
            token = verify_token
            msg = Message('Verify your email address', sender='burakcalagoz@gmail.com', recipients=[email])
            msg.body = f'Please click on this link to verify your email address: {url_for("auth.verify_email", token=token, _external=True)}'
            mail.send(msg)
            return True
    except Exception as exp:
        print(exp)
        return False


def hash_password(password):
    # Convert the password to a byte array
    password = bytes(password, 'utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Create a hash
    hashed_password = bcrypt.hashpw(password, salt)

    # Convert the byte array to a string and return
    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    # Taking user entered password and hashed password and encoding them
    user_bytes = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    # checking password
    return bcrypt.checkpw(user_bytes, hashed_password)


def create_token(token_type, user_id, session_key, role, email=None):
    """
    Create JWT token of the given type for the given user id and email
    """
    if token_type == "access":
        # Access token expires in 15 minutes
        expire_time = datetime.utcnow() + timedelta(minutes=15)
    elif token_type == "refresh":
        # Refresh token expires in 30 days
        expire_time = datetime.utcnow() + timedelta(days=30)
    elif token_type == "verify":
        # Email verification token expires in 24 hours
        expire_time = datetime.utcnow() + timedelta(hours=24)
    else:
        raise ValueError("Invalid token type")

    # Create the payload
    payload = {
        "user_id": user_id,
        "type": token_type,
        "exp": expire_time,
        "iat": datetime.utcnow(),
        "session_key": session_key,
        "role": role,
    }

    if email is not None:
        payload["email"] = email

    # Create the token
    token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")

    return token


def decode_token(token) -> dict:
    """
    Decode the JWT token and return the payload
    """
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # The token has expired
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        # The token is invalid
        raise ValueError("Token is invalid")

    # Check if the token contains the required fields
    required_fields = ["user_id", "type", "exp", "iat", "session_key", "role"]
    if any(field not in payload for field in required_fields):
        raise ValueError("Token is missing required fields")

    # Get the user_id, token_type, expiration and creation times from the payload
    user_id = payload["user_id"]
    token_type = payload["type"]
    exp_time = datetime.utcfromtimestamp(payload["exp"])
    iat_time = datetime.utcfromtimestamp(payload["iat"])
    session_key = payload["session_key"]
    role = payload["role"]

    # Get the email if it exists in the payload
    email = payload.get("email")

    # Create the token_info dictionary
    token_info = {
        "user_id": user_id,
        "type": token_type,
        "exp_time": exp_time,
        "iat_time": iat_time,
        "session_key": session_key,
        "role": role,
        "email": email,
    }

    return token_info
