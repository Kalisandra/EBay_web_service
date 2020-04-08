from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user

from webapp.model import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.ebay_search.views import blueprint as search_blueprint
from webapp.user.models import User
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


    @app.route('/')
    def index():
        if current_user.is_authenticated and current_user.token_status:
            return redirect(url_for('search.search'))
        elif (current_user.is_authenticated and not current_user.token_status):
            return redirect(url_for('user.redirect_user'))
        title = "Добро пожаловать на сайт"
        return render_template('index_page/main_index.html', page_title=title)

    return app
