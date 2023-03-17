from db.product import db_get_all_products, db_add_new_product, db_update_product, db_delete_product
from schemas.product import validate_json, product_schema
from flask import request, jsonify
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
        return jsonify({'error': f'{ex}'}), 500

    else:
        return products_json, 200


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


@validate_json(product_schema)
def add_new_product():
    try:
        new_product = request.json
        # Generated random product_id using uuid7
        create_new_product_id = str(uuid7().hex)
        new_product['id'] = create_new_product_id

        if not is_base64(new_product['image_url']):
            return jsonify({'message': 'image_url is not base64!'}), 400

        if db_add_new_product(new_product) == 1:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500

    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500


@validate_json(product_schema)
def update_product():
    try:
        product_id = request.args.get('product-id')

        updated_product = request.json

        if db_update_product(updated_product, product_id) == 1:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500


def delete_product():
    try:
        deleted_product_id = request.args.get('product-id')

        if db_delete_product(deleted_product_id) == 1:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500
