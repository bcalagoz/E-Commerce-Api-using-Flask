from flask import Blueprint
from controllers.auth import sign_up, login, logout


auth_bp = Blueprint('user', __name__)

auth_bp.route('/sign-up', methods=['GET', 'POST'])(sign_up)
auth_bp.route('/login', methods=['GET', "POST"])(login)
auth_bp.route('/logout', methods=['GET', "POST"])(logout)





