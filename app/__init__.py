__author__ = 'ash975@live.com'

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_moment import Moment

from .config import config
from .models import User
from .util import bson_obj_id

mongo = PyMongo()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    user = None
    db_user = mongo.db['user_current'].find_one({"_id": bson_obj_id(user_id)})
    if db_user is not None:
        user_id = db_user.pop('_id')
        user = User(user_id, extras=db_user)
    return user


def create_app(config_name='dev'):
    app = Flask(__name__)
    Bootstrap(app)
    Moment(app)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    mongo.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = '欢迎使用，请登录'


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from app.api import api as api_blueprint
    # app.register_blueprint(api_blueprint)

    from app.users import users as users_blueprint
    app.register_blueprint(users_blueprint,  url_prefix='/users')

    from app.setting import setting as setting_blueprint
    app.register_blueprint(setting_blueprint, url_prefix='/setting')

    from app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

def init_template_method(app):
    @app.context_processor
    def button_onload():
        pass
