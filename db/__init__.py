from flask import jsonify
import psycopg2
import os


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            database=os.environ.get('POSTGRES_DATABASE'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'))
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500
    else:
        return conn


def execute_without_commit(conn, cursor, sql, args=None):
    try:
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)

        row_count = cursor.rowcount

    except Exception as exp:
        print(exp)
        if conn:
            close(conn, cursor)
        return False, -1
    else:
        return True, row_count


def close(conn, cursor):
    """
    A method used to close connection of postgresql.
    :param conn:
    :param cursor:
    :return:
    """
    cursor.close()
    conn.close()


def get_connection_conn_cursor():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

    except Exception as exp:
        print(exp)
        return None, None
    else:
        return conn, cursor


def commit_without_execute(conn, cursor):
    try:
        conn.commit()
        if conn:
            close(conn, cursor)

        row_count = cursor.rowcount
    except Exception as exp:
        print(exp)
        if conn:
            close(conn, cursor)
        return False, -1
    else:
        return False, row_count


conn, cur = get_connection_conn_cursor()
# Open a cursor to perform database operations

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS users ('
            'id TEXT PRIMARY KEY,'
            'first_name VARCHAR(50) NOT NULL,'
            'last_name VARCHAR(50) NOT NULL,'
            'email VARCHAR(100) UNIQUE NOT NULL,'
            'password VARCHAR(255) NOT NULL,'
            'role VARCHAR(50) NOT NULL,'
            'is_verified BOOLEAN NOT NULL DEFAULT FALSE,'
            'address VARCHAR(255),'
            'city VARCHAR(50),'
            'state VARCHAR(50),'
            'zip_code VARCHAR(10),'
            'phone VARCHAR(20));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS auth ('
            'id TEXT PRIMARY KEY,'
            'user_id TEXT REFERENCES users(id),'
            'session_key TEXT NOT NULL,'
            'token_type VARCHAR(100) NOT NULL,'
            'browser TEXT,'
            'device TEXT,'
            'os TEXT,'
            'ip_address TEXT,'
            'location TEXT,'
            'created_at TIMESTAMP NOT NULL DEFAULT NOW());'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS stores ('
            'id TEXT PRIMARY KEY,'
            'name VARCHAR(100) NOT NULL,'
            'description TEXT,'
            'user_id TEXT REFERENCES users(id),'
            'created_at TIMESTAMP NOT NULL DEFAULT NOW(),'
            'is_active BOOLEAN NOT NULL DEFAULT TRUE );'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS products ('
            'id TEXT PRIMARY KEY,'
            'name VARCHAR(100) NOT NULL,'
            'description TEXT,'
            'price NUMERIC(10, 2) NOT NULL,'
            'image_url TEXT,'
            'created_at TIMESTAMP NOT NULL DEFAULT NOW(),'
            'is_active BOOLEAN NOT NULL DEFAULT TRUE,'
            'shop_id TEXT REFERENCES stores(id));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS orders ('
            'id TEXT PRIMARY KEY,'
            'customer_id TEXT REFERENCES users(id),'
            'shop_id TEXT REFERENCES stores(id),'
            'order_date TIMESTAMP NOT NULL DEFAULT NOW(),'
            'total_price NUMERIC(10, 2) NOT NULL,'
            'status VARCHAR(50) NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS order_items ('
            'id TEXT PRIMARY KEY,'
            'order_id TEXT REFERENCES orders(id),'
            'product_id TEXT REFERENCES products(id),'
            'quantity INTEGER NOT NULL,'
            'price NUMERIC(10, 2) NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS categories ('
            'id TEXT PRIMARY KEY,'
            'name VARCHAR(50) UNIQUE NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS product_categories ('
            'id TEXT PRIMARY KEY,'
            'product_id TEXT REFERENCES products(id),'
            'category_id TEXT REFERENCES categories(id));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS reviews ('
            'id TEXT PRIMARY KEY,'
            'customer_id TEXT REFERENCES users(id),'
            'product_id TEXT REFERENCES products(id),'
            'rating INTEGER NOT NULL,'
            'comment TEXT,'
            'review_date TIMESTAMP NOT NULL DEFAULT NOW());'
            )

conn.commit()
cur.close()
conn.close()
