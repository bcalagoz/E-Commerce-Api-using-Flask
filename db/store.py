from db import get_db_connection


def db_get_all_stores():
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute(query='SELECT * FROM stores')
    stores = cur.fetchall()

    cur.close()
    conn.close()

    return stores


def db_add_new_store(new_store):
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute('INSERT INTO stores (name, description, user_id)'
                'VALUES (%s, %s, %s)',
                (new_store['name'],
                 new_store['description'],
                 new_store['user_id'])  # TODO user_id tokendan gelicek
                )

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()

    return row_count


def db_update_store(updated_store, store_id):
    conn = get_db_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute('UPDATE stores '
                'SET name = %s, description = %s, user_id = %s '
                'WHERE id = %s',
                (updated_store['name'],
                 updated_store['description'],
                 updated_store['user_id'],
                 store_id)  # TODO user_id tokendan gelicek
    )

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()

    return row_count


def db_delete_store():
    return "Delete Stores", 200
