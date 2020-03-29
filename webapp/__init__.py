from flask import Flask
from flask_login import LoginManager

from webapp.model import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.ebay_search.views import blueprint as search_blueprint
from webapp.user.models import User
from webapp.ebay_search.models import Ebay_Categories
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(search_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
