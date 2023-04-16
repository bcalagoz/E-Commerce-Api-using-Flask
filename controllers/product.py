from db.product import Product
from schemas.product import new_product_schema, update_product_schema
from schemas import validate_json
from controllers import required_roles
from flask import request, jsonify
import base64


def get_all_products():
    try:
        products = Product.get_all_products()
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'products': [product.__dict__ for product in products]}), 200


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


@required_roles(["admin", "user"])
@validate_json(new_product_schema)
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


@validate_json(update_product_schema)
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
