from flask import request, jsonify
from db.store import Store


def get_all_stores():
    try:
        stores = Store.get_all_stores()
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500
    else:
        return jsonify({'stores': [store.__dict__ for store in stores]}), 200


def create_store():
    try:
        data = request.get_json()

        if Store.create_store(**data):
            return jsonify({'message': 'Store created successfully'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500

    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500


def update_store():
    try:
        store_id = request.args.get('store-id')
        data = request.get_json()
        data['id'] = store_id
        store = Store(**data)
        result = store.update_store(store_id, data['name'], data['description'], data['user_id'], data['is_active'])
        if result:
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500


def delete_store():
    try:
        store_id = request.args.get('store-id')

        if Store.delete_store(store_id):
            return jsonify({'message': 'Operation completed successfully.'}), 201
        else:
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500

