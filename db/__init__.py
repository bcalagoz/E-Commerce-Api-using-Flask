import os
import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="e-commerce",
        user="postgres",
        password="zxzx")

    return connection


conn = get_db_connection()
# Open a cursor to perform database operations
cur = conn.cursor()

# These statements to ensure that any existing tables with the same names are dropped before creating new ones
# cur.execute('DROP TABLE IF EXISTS reviews CASCADE;'
#             'DROP TABLE IF EXISTS product_categories CASCADE;'
#             'DROP TABLE IF EXISTS categories CASCADE;'
#             'DROP TABLE IF EXISTS order_items CASCADE;'
#             'DROP TABLE IF EXISTS orders CASCADE;'
#             'DROP TABLE IF EXISTS products CASCADE;'
#             'DROP TABLE IF EXISTS stores CASCADE;'
#             'DROP TABLE IF EXISTS users CASCADE;'
#             )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS users ('
            'id SERIAL PRIMARY KEY,'
            'first_name VARCHAR(50) NOT NULL,'
            'last_name VARCHAR(50) NOT NULL,'
            'email VARCHAR(100) UNIQUE NOT NULL,'
            'password VARCHAR(255) NOT NULL,'
            'address VARCHAR(255),'
            'city VARCHAR(50),'
            'state VARCHAR(50),'
            'zip_code VARCHAR(10),'
            'phone VARCHAR(20));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS stores ('
            'id SERIAL PRIMARY KEY,'  # TODO https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
            'name VARCHAR(100) NOT NULL,'
            'description TEXT,'
            'user_id INTEGER REFERENCES users(id),'
            'created_at TIMESTAMP NOT NULL DEFAULT NOW(),'
            'is_active BOOLEAN NOT NULL DEFAULT TRUE );'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS products ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR(100) NOT NULL,'
            'description TEXT,'
            'price NUMERIC(10, 2) NOT NULL,'
            'image_url VARCHAR(255),'
            'created_at TIMESTAMP NOT NULL DEFAULT NOW(),'
            'is_active BOOLEAN NOT NULL DEFAULT TRUE,'
            'shop_id INTEGER REFERENCES stores(id));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS orders ('
            'id SERIAL PRIMARY KEY,'
            'customer_id INTEGER REFERENCES users(id),'
            'shop_id INTEGER REFERENCES stores(id),'
            'order_date TIMESTAMP NOT NULL DEFAULT NOW(),'
            'total_price NUMERIC(10, 2) NOT NULL,'
            'status VARCHAR(50) NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS order_items ('
            'id SERIAL PRIMARY KEY,'
            'order_id INTEGER REFERENCES orders(id),'
            'product_id INTEGER REFERENCES products(id),'
            'quantity INTEGER NOT NULL,'
            'price NUMERIC(10, 2) NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS categories ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR(50) UNIQUE NOT NULL);'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS product_categories ('
            'id SERIAL PRIMARY KEY,'
            'product_id INTEGER REFERENCES products(id),'
            'category_id INTEGER REFERENCES categories(id));'
            )

# Execute a command: this creates a new table
cur.execute('CREATE TABLE IF NOT EXISTS reviews ('
            'id SERIAL PRIMARY KEY,'
            'customer_id INTEGER REFERENCES users(id),'
            'product_id INTEGER REFERENCES products(id),'
            'rating INTEGER NOT NULL,'
            'comment TEXT,'
            'review_date TIMESTAMP NOT NULL DEFAULT NOW());'
            )

conn.commit()
cur.close()
conn.close()
