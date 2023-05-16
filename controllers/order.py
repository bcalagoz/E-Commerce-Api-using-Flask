from db.order import Order
from db.product import Product
from flask import jsonify, request
from schemas.order import order_schema
from schemas import validate_json
from controllers import required_roles
from create_app.cache import cache


@cache.cached(timeout=50)
@required_roles(["admin"])
def get_all_orders(current_user):
    try:
        orders = Order.get_all_orders()
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'orders': orders}), 200


@required_roles(["admin", "user"])
@validate_json(order_schema)
def add_new_order(current_user):
    try:
        new_order = request.json
        if Order.create_order(**new_order):
            return jsonify({'message': 'Order created successfully'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user"])
def update_order():
    pass


@required_roles(["admin", "user"])
def delete_order():
    try:
        order_id = request.args.get('order-id')

        if Order.delete_order(order_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user"])
def add_item(current_user):
    try:
        data = request.get_json()
        product = Product.get_product_by_id(data["product_id"])
        order = Order.get_order_by_id(data["order_id"])
        if not product or not order:
            return jsonify({'error': 'product or order nor found!'}), 400

        if Order.add_item(**data):
            return jsonify({'message': 'Item successfully added!'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user"])
def delete_item():
    try:
        data = request.get_json()

        if Order.delete_item(**data):
            return jsonify({'message': 'Item successfully deleted!'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500



