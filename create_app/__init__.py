import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from routes.auth import auth_bp
from routes.order import order_bp
from routes.product import product_bp
from routes.store import store_bp


load_dotenv()


def create_app():
    app = Flask(__name__)
    mail = Mail()
    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # stuff
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')

    mail.init_app(app)
    app.extensions['mail'].debug = 0
    # more stuff
    return app