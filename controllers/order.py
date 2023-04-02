from db.order import Order
from db.product import Product
from flask import jsonify, request
from schemas.order import order_schema
from schemas import validate_json


def get_all_orders():
    try:
        orders = Order.get_all_orders()
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'orders': [order.__dict__ for order in orders]}), 200


@validate_json(order_schema)
def add_new_order():
    try:
        new_order = request.json
        if Order.create_order(**new_order):
            return jsonify({'message': 'Order created successfully'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def update_order():
    pass


def delete_order():
    try:
        order_id = request.args.get('order-id')

        if Order.delete_order(order_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def add_item():
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




