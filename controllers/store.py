import db
from db.store import db_get_all_stores, db_add_new_store, db_delete_store, db_update_store
from flask import request
from flask_expects_json import expects_json

# TODO hata durumlarınnı try catch ile ayarlaaa
# TODO logonun base64 olup olmadığını kotrol et


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
                    "user_id": store[3]
                }
            )

    except Exception as ex:
        print(ex)
        message = {'message': f'Error: {ex}'}
        return message, 500

    else:
        return stores_json, 200

# TODO schema dosyası oluştur shemaları ekle
schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'minLength': 4},
        'description': {'type': 'string'},
        'user_id': {'type': 'string'}
    },
    'required': ['name', 'description', 'user_id']
}


@expects_json(schema)
def add_new_store():
    new_store = request.json

    if db_add_new_store(new_store) == 1:
        return {"message": "OK"}, 201
    else:
        return {"message": "ERROR"}, 500


def update_store():
    store_id = request.args.get('store-id')

    updated_store = request.json

    if db_update_store(updated_store, store_id) == 1:
        return {"message": "OK"}, 201
    else:
        return {"message": "ERROR"}, 500


def delete_store():
    del_store_data = request.json
    print(del_store_data)
    return del_store_data




