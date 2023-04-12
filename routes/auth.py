from flask import Blueprint
from controllers.auth import sign_up, login, logout, refresh, verify, verify_email


auth_bp = Blueprint('user', __name__)

auth_bp.route('/sign-up', methods=["GET", "POST"])(sign_up)
auth_bp.route('/login', methods=["GET", "POST"])(login)
auth_bp.route('/logout', methods=["GET", "POST"])(logout)
auth_bp.route('/verify/<token>', methods=["GET"])(verify_email)
auth_bp.route('/refresh', methods=["GET"])(refresh)
auth_bp.route('/verify', methods=["GET"])(verify)







