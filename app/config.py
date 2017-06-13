import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    SECRET_KEY = os.urandom(24)
    MAIL_SENDER = ''
    MAIL_SUBJEXT_PREFIX = ''

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'aircleaner'

    @staticmethod
    def init_app(app):
        # from flask_pymongo import PyMongo
        from flask_pymongo import PyMongo
        app = PyMongo(app)
        return app


config = {
    'dev': DevConfig,
}
