from db.product import Product
from schemas.product import new_product_schema, update_product_schema
from schemas import validate_json
from controllers import required_roles
from flask import request, jsonify
from utils.functions import is_base64
from create_app.cache import cache


@cache.cached(timeout=50)
def get_all_products():
    try:
        products = Product.get_all_products()
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'products': [product.__dict__ for product in products]}), 200


@required_roles(["admin", "user"])
@validate_json(new_product_schema)
def add_new_product(current_user):
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


@required_roles(["admin", "user"])
@validate_json(update_product_schema)
def update_product():  # update fonksiyonlarında PATCH metodunu kullanabilir miyim?
    try:
        product_id = request.args.get('product-id')
        data = request.get_json()
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


@required_roles(["admin", "user"])
def delete_product():
    try:
        product_id = request.args.get('product-id')

        if Product.delete_product(product_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
