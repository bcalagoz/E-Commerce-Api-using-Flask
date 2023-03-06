from flask import Blueprint
from controllers.store import get_all_stores, add_new_store, update_store, delete_store

store_bp = Blueprint('store', __name__)

store_bp.route('/', methods=['GET'])(get_all_stores)
store_bp.route('/', methods=['POST'])(add_new_store)
store_bp.route('/', methods=['PUT'])(update_store)
store_bp.route('/', methods=['DELETE'])(delete_store)

