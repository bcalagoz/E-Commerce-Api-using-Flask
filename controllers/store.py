from flask import request, jsonify
from db.store import Store
from schemas.store import create_store_schema, update_store_schema
from schemas import validate_json
from create_app.cache import cache
from controllers import required_roles


@cache.cached(timeout=50)
def get_all_stores():
    try:
        stores = Store.get_all_stores()
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'stores': [store.__dict__ for store in stores]}), 200


@cache.cached(timeout=50)
def get_store_by_id(id):
    try:
        store = Store.get_store_by_id(id)
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'store': store.__dict__}), 200


@required_roles(["admin", "user"])
@validate_json(create_store_schema)
def create_store(current_user):
    try:
        data = request.get_json()
        data['user_id'] = current_user['user_id']

        if Store.create_store(**data):
            return jsonify({'message': 'Store created successfully'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500

    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user"])
@validate_json(update_store_schema)
def update_store(current_user):
    try:
        store_id = request.args.get('store-id')
        store = Store.get_store_by_id(store_id)
        if not store:
            return jsonify({'error': 'Store is not found!'}), 400

        if store.user_id != current_user['user_id']:
            return jsonify({'error': 'This is not your store!'}), 400

        data = request.get_json()
        result = Store.update_store(store_id, data['name'], data['description'], current_user['user_id'], data['is_active'])
        if result:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@required_roles(["admin", "user"])
def delete_store(current_user):
    try:
        store_id = request.args.get('store-id')
        store = Store.get_store_by_id(store_id)
        if not store:
            return jsonify({'error': 'Store is not found!'}), 400

        if store.user_id != current_user['user_id']:
            return jsonify({'error': 'This is not your store!'}), 400

        if Store.delete_store(store_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

