from flask import Blueprint
from controllers.product import get_all_products, add_new_product, update_product, delete_product

product_bp = Blueprint('product', __name__)

product_bp.route('/', methods=['GET'])(get_all_products)
product_bp.route('/', methods=['POST'])(add_new_product)
product_bp.route('/', methods=['PUT'])(update_product)
product_bp.route('/', methods=['DELETE'])(delete_product)
