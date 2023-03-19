from db.product import Product
from schemas.product import validate_json, product_schema
from flask import request, jsonify
import base64


def get_all_products():
    try:
        products = Product.get_all_products()
        products_json = {"products": []}
        # convert array to json TODO make it better
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
        return jsonify({'error': str(ex)}), 500

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

        if not is_base64(new_product['image_url']):
            return jsonify({'message': 'image_url is not base64 encoded!'}), 400

        if Product.create_product(**new_product):
            return jsonify({'message': 'Product created successfully'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


#@validate_json(product_schema)
def update_product():  # update fonksiyonlarında PATCH metodunu kullanabilir miyim?
    try:
        product_id = request.args.get('product-id')
        data = request.get_json()
        print(data.get('image_url'))
        if data.get('image_url'):
            if not is_base64(data['image_url']):
                return jsonify({'message': 'image_url is not base64!'}), 400
        result = Product.update_product(product_id, **data)
        if result:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def delete_product():
    try:
        product_id = request.args.get('product-id')

        if Product.delete_product(product_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
