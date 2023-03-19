from db import get_db_connection
import uuid


class Product:
    def __init__(self, id, name, description, price, image_url, created_at=None, is_active=True, shop_id=not None):
        # shop_id = not None kısmını düzelt
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
        products = [Product(*data) for data in product_data]
        print(products)
        cur.close()
        conn.close()
        return products

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

    @staticmethod
    def get_product_by_id(id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE id = %s", (id,))
        product_data = cur.fetchone()
        if product_data:
            product = Product(*product_data)
        else:
            product = None
        cur.close()
        conn.close()

        return product

    @staticmethod
    def update_product(id, name=None, description=None, price=None, image_url=None, shop_id=None, is_active=None):
        conn = get_db_connection()
        cur = conn.cursor()
        # Get the product to update
        product = Product.get_product_by_id(id)
        if product:
            # Update the product fields if provided
            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if price is not None:
                product.price = price
            if image_url is not None:
                product.image_url = image_url
            if shop_id is not None:
                product.shop_id = shop_id
            if is_active is not None:
                product.is_active = is_active

            # Update the product in the database
            cur.execute("UPDATE products SET name = %s, description = %s, price = %s, image_url = %s, shop_id = %s, "
                        "is_active = %s WHERE id = %s",
                        (product.name, product.description, product.price, product.image_url, product.shop_id,
                         product.is_active, id))
            conn.commit()
            cur.close()
            conn.close()
            return product
        else:
            cur.close()
            conn.close()

            return None

    @staticmethod
    def delete_product(id):
        conn = get_db_connection()
        cur = conn.cursor()
        product = Product.get_product_by_id(id)
        if product:
            cur.execute("DELETE FROM products WHERE id = %s", (id,))
            conn.commit()
            cur.close()
            conn.close()

            return product
        else:
            cur.close()
            conn.close()

            return None
