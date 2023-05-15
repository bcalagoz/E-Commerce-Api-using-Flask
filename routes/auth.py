from flask import Blueprint
from controllers.auth import sign_up, login, logout, refresh, verify, verify_email, get_all_sessions, get_sessions_by_user_id, ban_user


auth_bp = Blueprint('auth', __name__)

auth_bp.route('/sign-up', methods=["GET", "POST"])(sign_up)
auth_bp.route('/login', methods=["GET", "POST"])(login)
auth_bp.route('/logout', methods=["GET", "POST"])(logout)
auth_bp.route('/verify/<token>', methods=["GET"])(verify_email)
auth_bp.route('/refresh', methods=["GET"])(refresh)
auth_bp.route('/verify', methods=["GET"])(verify)
auth_bp.route('/session', methods=["GET"])(get_all_sessions)
auth_bp.route('/session/current', methods=["GET"])(get_sessions_by_user_id)
auth_bp.route('/ban', methods=["GET"])(ban_user)









