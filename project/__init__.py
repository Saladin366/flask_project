import datetime as dt
import locale

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

LOGIN = 'Пожалуйста, авторизуйтесь, чтобы получить доступ к этой странице'

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = LOGIN


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app,  db)
    login_manager.init_app(app)

    from .auth.views import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .blog.views import bp as blog_blueprint
    app.register_blueprint(blog_blueprint)

    locale.setlocale(locale.LC_ALL, 'ru-Ru')

    @app.context_processor
    def year():
        return {'year': dt.date.today().year}

    return app
