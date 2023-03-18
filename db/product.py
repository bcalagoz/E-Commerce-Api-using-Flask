from db import get_db_connection
import uuid



class Product:
    def __init__(self, id, name, description, price, image_url, shop_id, created_at=None, is_active=True):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.shop_id = shop_id
        self.created_at = created_at
        self.is_active = is_active

    @staticmethod
    def get_all_products():
        conn = get_db_connection()
        # Open a cursor to perform database operations
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        product_data = cur.fetchall()
        # products = [Product(*data) for data in product_data]
        cur.close()
        conn.close()
        return product_data

    @staticmethod
    def create_product(name, description, price, image_url, shop_id):
        conn = get_db_connection()
        cur = conn.cursor()
        id = uuid.uuid4().hex
        cur.execute('INSERT INTO products (id, name, description, price, image_url, shop_id) '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (id, name, description, price, image_url, shop_id))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count


# def db_get_all_products():
#     conn = get_db_connection()
#     # Open a cursor to perform database operations
#     cur = conn.cursor()
#
#     cur.execute(query='SELECT * FROM products')
#     products = cur.fetchall()
#
#     cur.close()
#     conn.close()
#
#     return products


def db_add_new_product(new_product):
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute('INSERT INTO products (id, name, description, price, image_url, shop_id)'
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (new_product['id'],
                 new_product['name'],
                 new_product['description'],
                 new_product['price'],
                 new_product['image_url'],
                 new_product['shop_id'])
                )

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()

    return row_count


def db_update_product(updated_product, product_id):
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute('UPDATE products '
                'SET name = %s, description = %s, price = %s,  image_url = %s, shop_id = %s '
                'WHERE id = %s',
                (updated_product['name'],
                 updated_product['description'],
                 updated_product['price'],
                 updated_product['image_url'],
                 updated_product['shop_id'],
                 product_id)
                )

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()

    return row_count


def db_delete_product(deleted_product_id):
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (deleted_product_id,))

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()

    return row_count
