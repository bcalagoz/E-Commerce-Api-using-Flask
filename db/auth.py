from db import get_db_connection


class User:
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = 'customer'
        self.is_verified = False
        self.address = None
        self.city = None
        self.state = None
        self.zip_code = None
        self.phone = None

    def add_new_user(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (id, first_name, last_name, email, password, role) '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (self.id, self.first_name, self.last_name, self.email, self.password, self.role,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count


class Auth:
    def __init__(self, id, user_id, session_key, token_type, token):
        self.id = id
        self.user_id = user_id
        self.session_key = session_key
        self.token_type = token_type
        self.token = token

    def add_token_to_db(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO auth (id, user_id, session_key, token_type, token) '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (self.id, self.user_id, self.session_key, self.token_type, self.token,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count
