from flask import Flask
from routes.store import store_bp
from routes.product import product_bp
from routes.auth import auth_bp
from routes.order import order_bp

app = Flask(__name__)

app.register_blueprint(store_bp, url_prefix='/store')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(auth_bp, url_prefix='/auth')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
