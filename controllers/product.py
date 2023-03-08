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
                    "shop_id": product[5],
                    "created_at": product[6],
                    "is_active": product[7],
                }
            )

    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500

    else:
        return products_json, 200


def add_new_product():
    pass


def update_product():
    pass


def delete_product():
    pass