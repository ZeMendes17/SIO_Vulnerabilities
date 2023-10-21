from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = "shhhsecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)
    ma = Marshmallow(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        print(e)
        return render_template("404.html")

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .register import register as register_blueprint

    app.register_blueprint(register_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .shop import shops as shops_blueprint

    app.register_blueprint(shops_blueprint)

    from .product import products as product_blueprint

    app.register_blueprint(product_blueprint)

    from .checkout import checkout as checkout_blueprint

    app.register_blueprint(checkout_blueprint)

    from .utils import utl as utils_blueprint

    app.register_blueprint(utils_blueprint)

    from .cart import shopping_cart as cart_blueprint

    app.register_blueprint(cart_blueprint)

    from .profile import profile as profile_blueprint

    app.register_blueprint(profile_blueprint)

    from .wishList import wish_list as wish_list_blueprint

    app.register_blueprint(wish_list_blueprint)

    from .orders import orders as orders_blueprint

    app.register_blueprint(orders_blueprint)

    from .admin import admin as admin_blueprint

    app.register_blueprint(admin_blueprint)

    return app
