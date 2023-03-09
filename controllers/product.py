from db.product import db_get_all_products, db_add_new_product, db_update_product, db_delete_product
from flask import request
from flask_expects_json import expects_json
from uuid6 import uuid7
import base64


def get_all_products():
    try:
        products = db_get_all_products()
        products_json = {"products": []}
        # convert array to json
        for product in products:
            products_json["products"].append(
                {
                    "id": product[0],
                    "name": product[1],
                    "description": product[2],
                    "price": product[3],
                    "image_url": product[4],
                    "created_at": product[5],
                    "is_active": product[6],
                    "shop_id": product[7],
                }
            )
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500

    else:
        return products_json, 200


add_new_product_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'price': {'type': 'string'},
        'image_url': {'type': 'string'},
        'shop_id': {'type': 'string'},
    },
    'required': ['name', 'description', 'price', 'image_url', 'shop_id']
}


def is_base64(s):
    try:
        # Attempt to decode the data from base64
        if isinstance(s, str):
            # If the data is a string, convert it to bytes first
            s = bytes(s, 'utf-8')
        # Check if the decoded data can be encoded back to base64
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        # If an exception is thrown during the decoding or encoding process, return False
        return False


@expects_json(add_new_product_schema)
def add_new_product():
    try:
        new_product = request.json
        # Generated random product_id using uuid7
        create_new_product_id = str(uuid7().hex)
        new_product['id'] = create_new_product_id
        if is_base64(new_product['image_url']):
            if db_add_new_product(new_product) == 1:
                return {"message": "OK"}, 201
            else:
                return {"message": "ERROR"}, 500
        else:
            return {"message": "ERROR: image_url is not base64!"}, 500
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500


def update_product():
    pass


def delete_product():
    pass