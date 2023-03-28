from flask import jsonify
import psycopg2


def get_db_connection():
    # TODO burayı düzelt
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="e-commerce",
            user="postgres",
            password="zxzx")
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500
    else:
        return connection


conn = get_db_connection()
# Open a cursor to perform database operations
cur = conn.cursor()

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
            'token TEXT NOT NULL,'
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
