from flask import Blueprint
from controllers.order import get_all_orders, add_new_order, update_order, delete_order, add_item

order_bp = Blueprint('order', __name__)

order_bp.route('/', methods=['GET'])(get_all_orders)
order_bp.route('/', methods=['POST'])(add_new_order)
order_bp.route('/', methods=['PUT'])(update_order)
order_bp.route('/item', methods=['PUT'])(add_item)
order_bp.route('/', methods=['DELETE'])(delete_order)
