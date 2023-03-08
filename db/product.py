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


def db_add_new_product():
    pass


def db_update_product():
    pass


def db_delete_product():
    pass
