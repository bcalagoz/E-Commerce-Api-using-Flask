from db.product import db_get_all_products, db_add_new_product, db_update_product, db_delete_product
from flask import request
from flask_expects_json import expects_json
from uuid6 import uuid7


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


@expects_json(add_new_product_schema)
def add_new_product():
    try:
        new_product = request.json
        # Generated random product_id using uuid7
        create_new_product_id = str(uuid7().hex)
        new_product['id'] = create_new_product_id

        if db_add_new_product(new_product) == 1:
            return {"message": "OK"}, 201
        else:
            return {"message": "ERROR"}, 500
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500


def update_product():
    pass


def delete_product():
    pass