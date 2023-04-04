from psycopg2.extras import execute_values

from db import get_db_connection
import uuid


class Order:
    def __init__(self, id, customer_id, shop_id, order_date=None, total_price="0", status="pending"):
        self.id = id
        self.customer_id = customer_id
        self.shop_id = shop_id
        self.order_date = order_date
        self.total_price = total_price
        self.status = status
        self.items = []

    @staticmethod
    def get_all_orders():
        conn = get_db_connection()
        cur = conn.cursor()

        orders = []
        cur.execute("SELECT * FROM orders;")
        order_data = cur.fetchall()

        for data in order_data:
            order = Order(*data)
            cur.execute("SELECT * FROM order_items WHERE order_id=%s;", (order.id,))
            item_data = cur.fetchall()
            for item in item_data:
                order.items.append({"id": item[0], "order_id": item[1], "product_id": item[2], "quantity": item[3], "price": item[4]})
            orders.append(order)

        cur.close()
        conn.close()
        return orders

    @staticmethod
    def create_order(customer_id, shop_id, total_price, status, items):
        conn = get_db_connection()
        cur = conn.cursor()
        order_id = uuid.uuid4().hex
        try:
            cur.execute('BEGIN')
            cur.execute('INSERT INTO orders (id, customer_id, shop_id, total_price, status) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (order_id, customer_id, shop_id, total_price, status,))
            # Generate a list of tuples containing the necessary information for each item
            item_values = [(uuid.uuid4().hex, order_id, item['product_id'], item['quantity'], item['price'])
                           for item in items]
            # Use execute_values to insert all items in a single query
            execute_values(cur, 'INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES %s',
                           item_values)
            cur.execute('COMMIT')
            row_count = cur.rowcount
            cur.close()
            conn.close()
            return row_count
        except Exception as ex:
            cur.execute('ROLLBACK')
            cur.close()
            conn.close()
            raise ex

    @staticmethod
    def get_order_by_id(id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE id = %s", (id,))
        order_data = cur.fetchone()
        if order_data:
            order = Order(*order_data)
        else:
            order = None
        cur.close()
        conn.close()

        return order

    @staticmethod
    def delete_order(id):
        conn = get_db_connection()
        cur = conn.cursor()
        order = Order.get_order_by_id(id)
        if order:
            try:
                cur.execute('BEGIN')
                cur.execute('DELETE FROM order_items WHERE order_id = %s', (id,))
                cur.execute('DELETE FROM orders WHERE id = %s', (id,))
                cur.execute('COMMIT')
                cur.close()
                conn.close()
                return order
            except Exception as ex:
                cur.execute('ROLLBACK')
                cur.close()
                conn.close()
                raise ex
        else:
            cur.close()
            conn.close()
            return None

    @staticmethod
    def add_item(order_id, product_id, quantity, price):
        conn = get_db_connection()
        cur = conn.cursor()
        item_id = uuid.uuid4().hex
        cur.execute('INSERT INTO order_items (id, order_id, product_id, quantity, price) '
                    'VALUES (%s, %s, %s, %s, %s)',
                    (item_id, order_id, product_id, quantity, price,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count

    @staticmethod
    def delete_item(order_id, product_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM order_items WHERE order_id = %s AND product_id = %s', (order_id, product_id,))
        conn.commit()
        row_count = cur.rowcount
        cur.close()
        conn.close()
        return row_count
