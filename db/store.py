import uuid
from db import get_db_connection
import psycopg2


class Store:
    def __init__(self, id, name, description, user_id, created_at=None, is_active=True):
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.created_at = created_at
        self.is_active = is_active

    @staticmethod
    def get_all_stores():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM stores")
        store_data = cur.fetchall()
        # Bu tuple'daki verileri kullanarak bir Store objesi oluşturmak için, *data ifadesi kullanılır.
        stores = [Store(*data) for data in store_data]
        cur.close()
        conn.close()
        return stores

    @staticmethod
    def create_store(name, description, user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        id = uuid.uuid4().hex
        cur.execute('INSERT INTO stores (id, name, description, user_id) '
                    'VALUES (%s, %s, %s, %s)',
                    (id, name, description, user_id,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count

    @staticmethod
    def get_store_by_id(id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM stores WHERE id = %s", (id,))
        store_data = cur.fetchone()
        if store_data:
            store = Store(*store_data)
        else:
            store = None
        cur.close()
        conn.close()

        return store

    @staticmethod
    def update_store(id, name=None, description=None, user_id=None, is_active=None):
        conn = get_db_connection()
        cur = conn.cursor()
        store = Store.get_store_by_id(id)
        if store:
            if name is not None:
                store.name = name
            if description is not None:
                store.description = description
            if user_id is not None:
                store.user_id = user_id
            if is_active is not None:
                store.is_active = is_active

            cur.execute("UPDATE stores SET name = %s, description = %s, is_active = %s WHERE id = %s",
                        (store.name, store.description, store.is_active, store.id))
            conn.commit()
            cur.close()
            conn.close()

            return store
        else:
            cur.close()
            conn.close()

            return None

    @staticmethod
    def delete_store(id):
        conn = get_db_connection()
        cur = conn.cursor()
        store = Store.get_store_by_id(id)
        if store:
            try:
                cur.execute('BEGIN')
                cur.execute('DELETE FROM products WHERE shop_id = %s', (id,))
                cur.execute('DELETE FROM stores WHERE id = %s', (id,))
                cur.execute('COMMIT')
                cur.close()
                conn.close()
                return store
            except (Exception, psycopg2.DatabaseError) as error:
                cur.execute('ROLLBACK')
                cur.close()
                conn.close()
                raise error
        else:
            cur.close()
            conn.close()
            return None
