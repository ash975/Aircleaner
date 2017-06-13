from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.util import bson_to_json
from app.util import bson_obj_id

import json


class User(UserMixin):

    def __init__(self, user_id, extras=None):
        self.id = user_id
        if extras is not None and isinstance(extras, dict):
            for name, attr in extras.items():
                setattr(self, name, attr)

    @staticmethod
    def gen_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password_hash, password):
        return check_password_hash(password_hash, password)

    def gen_auth_token(self, expiration):
        series = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return series.dumps(bson_to_json({"id": self.id}))

    @staticmethod
    def verify_auth_token(token):
        from app import mongo
        series = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = series.loads(token)
        except:
            return None
        dict_ = json.loads(data)
        return mongo.db.users.find_one({"_id": bson_obj_id(dict_['id']["$oid"])})


class Setting(object):
    pass



