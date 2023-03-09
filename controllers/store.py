import db
from db.store import db_get_all_stores, db_add_new_store, db_delete_store, db_update_store
from flask import request
from flask_expects_json import expects_json
from uuid6 import uuid7


def get_all_stores():
    try:
        stores = db_get_all_stores()
        stores_json = {"stores": []}
        # convert array to json
        for store in stores:
            stores_json["stores"].append(
                {
                    "id": store[0],
                    "name": store[1],
                    "description": store[2],
                    "user_id": store[3],
                    "created_at": store[4],
                    "is_active": store[5]
                }
            )

    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500

    else:
        return stores_json, 200


# TODO schema dosyası oluştur shemaları ekle
add_new_store_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'user_id': {'type': 'string'}
    },
    'required': ['name', 'description', 'user_id']
}


@expects_json(add_new_store_schema)
def add_new_store():
    try:
        new_store = request.json
        # Generated random store_id using uuid7
        create_new_store_id = str(uuid7().hex)
        new_store['id'] = create_new_store_id

        if db_add_new_store(new_store) == 1:
            return {"message": "OK"}, 201
        else:
            return {"message": "ERROR"}, 500
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500


update_store_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'user_id': {'type': 'string'}
    },
    'required': ['name', 'description', 'user_id']
}


@expects_json(update_store_schema)
def update_store():
    try:
        store_id = request.args.get('store-id')

        updated_store = request.json

        if db_update_store(updated_store, store_id) == 1:
            return {"message": "OK"}, 201
        else:
            return {"message": "ERROR"}, 500
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500


def delete_store():
    try:
        deleted_store_id = request.args.get('store-id')

        if db_delete_store(deleted_store_id) == 1:
            return {"message": "OK"}, 201
        else:
            return {"message": "ERROR"}, 500
    except Exception as ex:
        message = {'message': f'Error: {ex}'}
        return message, 500
