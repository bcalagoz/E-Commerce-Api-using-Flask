from db import get_db_connection


def db_get_all_products():
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute(query='SELECT * FROM products')
    products = cur.fetchall()

    cur.close()
    conn.close()

    return products


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


def db_update_product():
    pass


def db_delete_product():
    pass
