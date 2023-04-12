from db.auth import User, Auth
from flask import request, jsonify, url_for
import uuid
from schemas.auth import login_schema, sign_up_schema
from schemas import validate_json
from utils.functions import hash_password, check_password, create_token, decode_token
from controllers import auth_service
from datetime import datetime
from flask_mail import Mail, Message


# from app import mail


def refresh():
    """
    - refresh token ve user id auth tablosun kontrol et
    - varsa yeni refreesh token ve access token ver,
    - yeni access eski refresh
    - yoksa
    :return:
    """
    try:
        refresh_token = request.headers.get('Authorization')
        if refresh_token:
            token_info = decode_token(refresh_token)
            if token_info["type"] == "refresh":
                auth_data = Auth.get_token_by_session_key(token_info["session_key"])
                auth_data_json = {
                    "id": auth_data[0],
                    "user_id": auth_data[1],
                    "session_key": auth_data[2],
                    "type": auth_data[3],
                }
                if token_info["user_id"] == auth_data_json["user_id"] and token_info["session_key"] == auth_data_json[
                    "session_key"]:
                    access_token = create_token("access", auth_data_json["user_id"], auth_data_json["session_key"])
                    return {"access_token": access_token, "refresh_token": refresh_token}, 200
                else:
                    return jsonify({'error': 'Invalid token!'}), 400
            else:
                return jsonify({'error': 'Invalid token!'}), 400
        else:
            return jsonify({'error': 'Invalid token!'}), 400

    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def verify():
    """
    - verify token ve email auth tablosunda kontrol et.

    :return: yeni verify dön
    """
    pass


@validate_json(sign_up_schema)
def sign_up():
    new_account_data = request.get_json()
    return auth_service.sign_up(new_account_data)


@validate_json(login_schema)
def login():
    account_data = request.get_json()
    user = User.get_user_by_email(account_data['email'])
    if user:
        user_json = {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "email": user[3],
            "password": user[4],
            "is_verified": user[6],
        }
        if check_password(account_data['password'], user_json["password"]):
            if user_json["is_verified"]:
                session_key = uuid.uuid4().hex
                access_token = create_token("access", user_json["id"], session_key)
                refresh_token = create_token("refresh", user_json["id"], session_key)
                verify_token = create_token("verify", user_json["id"], session_key, user[3])
                tokens_data = [(uuid.uuid4().hex, user_json["id"], session_key, "refresh"),
                               (uuid.uuid4().hex, user_json["id"], session_key, "verify")]
                Auth.add_token_to_db(tokens_data)
                return {'access_token': access_token, 'refresh_token': refresh_token, 'verify_token': verify_token,
                        'user_id': user_json["id"]}, 200
            else:
                return jsonify({'error': 'Account is not verified!'}), 400
        else:
            return jsonify({'error': 'Wrong password, Please try again!'}), 400
    else:
        return jsonify({'error': 'The email that you have entered doesn\'t match any account!'}), 400


def logout():
    try:
        auth_token = request.headers.get('Authorization')

        if auth_token:
            token_info = decode_token(auth_token)
            # Check if the access token has expired
            # if token_info["exp_time"] < datetime.utcnow():
            #     raise ValueError("Access token has expired")
            session_key = token_info["session_key"]
            if Auth.delete_token(session_key):
                return jsonify({'message': 'Successful!'}), 200
            else:
                return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def verify_email(token):
    # verify token auth tablosunda varsa user
    try:
        token_data = decode_token(token)
        user_id = token_data["user_id"]
        if user_id and token_data["type"] == "verify":
            verify_token = Auth.get_verify_token_by_user_id(user_id)
            if verify_token:
                User.verify_user(user_id)
                return jsonify({'message': 'User successfully verified!'}), 200
        else:
            return jsonify({'message': 'Invalid verification link!'}), 400
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


# def send_verification_email(verify_token, email):
#     try:
#         token = verify_token
#         msg = Message('Verify your email address', sender='burakcalagoz@gmail.com', recipients=[email])
#         msg.body = f'Please click on this link to verify your email address: {url_for("verify_email", token=token, _external=True)}'
#         mail.send(msg)
#         return True
#     except Exception as exp:
#         print(exp)
#         return False
