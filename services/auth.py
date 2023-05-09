from db.auth import Auth, User
from db import get_connection_conn_cursor, execute_without_commit, commit_without_execute
from utils.functions import hash_password
import uuid
from flask import jsonify, json, request
from utils.functions import create_token, send_verification_email
from ua_parser import user_agent_parser
import requests


class AuthService:
    auth_db = None
    user_db = None

    def __init__(self):
        self.auth_db = Auth()
        self.user_db = User()

    def sign_up(self, new_account_data):
        try:
            new_account_data['password'] = hash_password(new_account_data['password'])
            new_account_data['id'] = uuid.uuid4().hex
            new_account_data['role'] = "unverified"

            if self.user_db.get_user_by_email(new_account_data['email']):
                return jsonify({'error': 'Email already exists!'}), 400

            conn, cur = get_connection_conn_cursor()
            query = 'INSERT INTO users (id, first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)'
            args = (new_account_data['id'], new_account_data['first_name'], new_account_data['last_name'], new_account_data['email'], new_account_data['password'], new_account_data['role'])

            if not execute_without_commit(conn, cur, query, args):
                raise Exception('Error executing SQL query')

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

            # Create session_key
            session_key = uuid.uuid4().hex

            access_token = create_token("access", new_account_data['id'], session_key, new_account_data['role'])
            refresh_token = create_token("refresh", new_account_data['id'], session_key, new_account_data['role'])
            verify_token = create_token("verify", new_account_data['id'], session_key, new_account_data['role'], new_account_data['email'])

            args = ((uuid.uuid4().hex, new_account_data['id'], session_key, "refresh", browser, device, os, ip_adress, location),
                    (uuid.uuid4().hex, new_account_data['id'], session_key, "verify", browser, device, os, ip_adress, location))
            for arg in args:
                query = 'INSERT INTO auth (id, user_id, session_key, token_type, browser, device, os, ip_address, location) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)'
                if not execute_without_commit(conn, cur, query, arg):
                    raise Exception('Error executing SQL query')

            if not commit_without_execute(conn, cur):
                raise Exception('Error committing transaction')

            send_verification_email(verify_token, new_account_data['email'])

            return {'access_token': access_token, 'refresh_token': refresh_token, 'verify_token': verify_token,
                    'user_id': new_account_data['id']}, 201

        except Exception as ex:
            return jsonify({'error': str(ex)}), 500

