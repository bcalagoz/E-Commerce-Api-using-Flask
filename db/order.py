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

    @staticmethod
    def get_all_orders():
        # TODO add items
        conn = get_db_connection()
        # Open a cursor to perform database operations
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders")
        order_data = cur.fetchall()
        orders = [Order(*data) for data in order_data]
        cur.close()
        conn.close()
        return orders

    @staticmethod
    def create_order(customer_id, shop_id, total_price, status, items):
        conn = get_db_connection()
        cur = conn.cursor()
        id = uuid.uuid4().hex
        try:
            cur.execute('BEGIN')
            cur.execute('INSERT INTO orders (id, customer_id, shop_id, total_price, status) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (id, customer_id, shop_id, total_price, status,))
            for item in items:
                item['id'] = uuid.uuid4().hex
                cur.execute('INSERT INTO order_items (id, order_id, product_id, quantity, price) '
                            'VALUES (%s, %s, %s, %s, %s)',
                            (item['id'], id, item['product_id'], item['quantity'], item['price'],))
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

