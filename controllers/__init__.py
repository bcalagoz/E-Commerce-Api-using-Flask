from services.auth import AuthService
from functools import wraps
from flask import request


auth_service = AuthService()


def required_roles():
    '''
    parametre olarak array gönder (admin,customer...)
    enum ile rol tanımla
    tokenda role gönder

    :return:
    '''
    def inner_function(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            try:

                token = request.headers.get('Authorization')

                route_name = request.path.split("/")[1]

                key_name = SERVICE_NAME + "-" + original_function._name_ + "-" + route_name + "-" + request.method

                role_list = user_roles_permissions[key_name]

                if not token:
                    return make_response({"message_code": MessageCode.MISSING_TOKEN_ERROR_MESSAGE}, 403)

                if token in [ProductionConfig.SECRET_KEYS.get("pmc_app"),
                             ProductionConfig.SECRET_KEYS.get("buildings"),
                             ProductionConfig.SECRET_KEYS.get("orders"),
                             ProductionConfig.SECRET_KEYS.get("regions"),
                             ProductionConfig.SECRET_KEYS.get("pm_public_api"),
                             ProductionConfig.SECRET_KEYS.get("reports")]:
                    return original_function(*args, **kwargs)

                public_key = ProductionConfig.SECRET_KEYS.get("paketmutfak")
                decoded = jwt.decode(token, public_key, algorithms=["HS256"])
                role_type = decoded.get("role_type")

                if role_type not in role_list:
                    return make_response({"message_code": MessageCode.UNAUTHORAZATION_ERROR_MESSAGE}, 403)

            except:
                return make_response({"message_code": MessageCode.UNAUTHORAZATION_ERROR_MESSAGE}, 403)
            else:
                return original_function(*args, **kwargs)
        return wrapper

    return inner_function