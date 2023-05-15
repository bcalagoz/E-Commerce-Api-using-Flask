from db.auth import User, Auth
from flask import request, jsonify, json
import uuid
from schemas.auth import login_schema, sign_up_schema
from schemas import validate_json
from utils.functions import check_password, create_token, decode_token
from controllers import auth_service
from controllers import required_roles
from ua_parser import user_agent_parser
import requests
from create_app.cache import cache
from create_app.redis import redis_conn


'''
drop session (user ve admin  göndermeli)
drop yaparken session a ait verileri sil database redise ekle
'''

'''
redis kullan
kullanıcı banlama endpointi olsun.(userid , ne kadar süre banlanacak ver kullanıcı banla)
redise koy
bir tane decoratör koy is_banned() redisten kontrol et
banlanma süresi ekle
user_id: {banın biteceği süre: }
'''
'''
resend verification mail
'''

'''
role değiştirme ekle
'''


@required_roles(["admin", "user", "unverified"])
def refresh():
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
    # TODO verified değil ise verifiy token gönder
    try:
        account_data = request.get_json()
        user = User.get_user_by_email(account_data['email'])
        if user:
            user_json = {
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "email": user[3],
                "password": user[4],
                "role": user[5],
                "is_verified": user[6],
            }
            if redis_conn.exists(user_json["id"]):
                return jsonify({'message': 'User is banned.'}), 403

            if check_password(account_data['password'], user_json["password"]):
                ua_string = request.user_agent.string
                parsed_string = user_agent_parser.Parse(ua_string)
                browser = parsed_string['user_agent']['family']  # browser
                device = parsed_string['device']['model']  # device
                os = parsed_string['os']['family']  # os
                ip_adress = request.remote_addr  # ip_address
                access_key = "4824fb5309db20b5a30db540c7066670"
                url = f'http://api.ipstack.com/{ip_adress}?access_key={access_key}&format=1'
                r = requests.get(url)
                j = json.loads(r.text)
                location = j['city']  # location

                session_key = uuid.uuid4().hex
                access_token = create_token("access", user_json["id"], session_key, user_json["role"])
                refresh_token = create_token("refresh", user_json["id"], session_key, user_json["role"])
                verify_token = create_token("verify", user_json["id"], session_key, user_json["role"], user_json["email"])
                tokens_data = [(uuid.uuid4().hex, user_json["id"], session_key, "refresh", browser, device, os, ip_adress, location),
                               (uuid.uuid4().hex, user_json["id"], session_key, "verify", browser, device, os, ip_adress, location)]
                Auth.add_token_to_db(tokens_data)
                return {'access_token': access_token, 'refresh_token': refresh_token, 'verify_token': verify_token,
                        'user_id': user_json["id"]}, 200
            else:
                return jsonify({'error': 'Wrong password, Please try again!'}), 400
        else:
            return jsonify({'error': 'The email that you have entered doesn\'t match any account!'}), 400
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user", "unverified"])
def logout(current_user):
    try:
        if Auth.delete_token(current_user['session_key']):
            return jsonify({'message': 'Successful!'}), 200
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def verify_email(token):
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


@cache.cached(timeout=50)
@required_roles(["admin"])
def get_all_sessions(current_user):
    try:
        auth_data = Auth.get_all_sessions()
        sessions = []

        for item in auth_data:
            session = {
                'id': item[0],
                'user_id': item[1],
                'session_key': item[2],
                'token_type': item[3],
                'browser': item[4],
                'device': item[5],
                'os': item[6],
                'ip_address': item[7],
                'location': item[8],
                'created_at': item[9],
            }
            sessions.append(session)
        return jsonify({'sessions': sessions}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user", "unverified"])
def get_sessions_by_user_id(current_user):
    try:
        auth_data = Auth.get_sessions_by_user_id(current_user['user_id'])
        sessions = []

        for item in auth_data:
            session = {
                'id': item[0],
                'user_id': item[1],
                'session_key': item[2],
                'token_type': item[3],
                'browser': item[4],
                'device': item[5],
                'os': item[6],
                'ip_address': item[7],
                'location': item[8],
                'created_at': item[9],
            }
            sessions.append(session)
        return jsonify({'sessions': sessions}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin"])
def ban_user(current_user):
    try:
        data = request.get_json()
        user_id = data['user_id']
        expiration_time = data['ex'] # expiration time is seconds

        if redis_conn.exists(user_id):
            return jsonify({'message': 'User has already banned.'}), 403

        redis_conn.set(data['user_id'], 'banned', ex=expiration_time)

        return jsonify({'message': f'User {user_id} is banned.'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
