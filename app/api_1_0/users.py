from app import mongo
from ..util import bson_to_json
from ..util import bson_obj_id
from flask import request
from flask.views import MethodView

from . import *

import json


class UserAPI(MethodView):
    def get(self, username):
        if username is not None:
            item = mongo.db['user_current'].find_one({'username': username})
            return bson_to_json(item)

        params = {}
        for key, value in request.args.items():
            if value:
                params["attributes." + key] = value.strip()
        cursor = mongo.db['user_current'].find(params)
        items={}
        for item in cursor:
            items.update({json.loads(bson_to_json(item))['username']: json.loads(bson_to_json(item))})
        return json.dumps(items)


user_view = UserAPI.as_view('user_api')
api.add_url_rule('/users/', defaults={'username': None}, view_func=user_view, methods=['GET', ])
api.add_url_rule('/users/<username>', view_func=user_view, methods=['GET',])
