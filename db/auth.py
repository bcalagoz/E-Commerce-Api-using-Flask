from db import get_db_connection, get_connection_conn_cursor
from psycopg2.extras import execute_values


class User:
    @staticmethod
    def add_new_user(id, first_name, last_name, email, password, role='unverified'):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (id, first_name, last_name, email, password, role) '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (id, first_name, last_name, email, password, role,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count

    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        if user_data:
            user = user_data
        else:
            user = None
        cur.close()
        conn.close()

        return user

    @staticmethod
    def verify_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("UPDATE users SET is_verified = %s, role = %s WHERE id = %s",
                    (True, "user", user_id))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count


class Auth:
    @staticmethod
    def add_token_to_db(tokens_data):
        conn, cur = get_connection_conn_cursor()
        cur = conn.cursor()
        execute_values(cur, 'INSERT INTO auth (id, user_id, session_key, token_type, browser, device, os, ip_address, location) VALUES %s',
                       tokens_data)
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count

    @staticmethod
    def get_token_by_session_key(session_key):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM auth WHERE session_key = %s", (session_key,))
        token_data = cur.fetchone()
        if not token_data:
            token_data = None

        cur.close()
        conn.close()

        return token_data

    @staticmethod
    def delete_token(session_key):
        conn = get_db_connection()
        cur = conn.cursor()
        token = Auth.get_token_by_session_key(session_key)
        if token:
            cur.execute("DELETE FROM auth WHERE session_key = %s", (session_key,))
            conn.commit()
            cur.close()
            conn.close()

            return token
        else:
            cur.close()
            conn.close()

            return None

    @staticmethod
    def get_verify_token_by_user_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM auth WHERE user_id = %s AND token_type = %s ", (user_id, "verify"))
        token_data = cur.fetchone()
        if not token_data:
            token_data = None

        cur.close()
        conn.close()

        return token_data
