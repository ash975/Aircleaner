from app import mongo
from ..util import bson_to_json
from ..util import bson_obj_id
from flask import request
from flask.views import MethodView

from . import *

import json


class DeviceAPI(MethodView):
    def get(self, device_name):
        if device_name is not None:
            item = mongo.db['device_current'].find_one({'device_name': device_name})
            return bson_to_json(item)

        params = {}
        for key, value in request.args.items():
            if value:
                params["attributes." + key] = value.strip()
        cursor = mongo.db['device_current'].find(params)
        items={}
        for item in cursor:
            items.update({json.loads(bson_to_json(item))['device_name']: json.loads(bson_to_json(item))})
        return json.dumps(items)

    def post(self, device_name):
        data = json.loads(request.data.decode())
        if device_name == "host":
            reset = data.get('reset')
            if reset:
                return json.dumps({'status': 9})
        if data:
            set_data = {'$set': json.loads(request.data.decode())}
        else:
            return json.dumps({'status': 3})
        if device_name is not None:
            mongo.db['device_current'].update_one({'device_name': device_name}, set_data)
            return json.dumps({'status': 0})
        return json.dumps({'status': 1})

    def put(self, device_name):
        data = json.loads(request.data.decode())
        if device_name == "host":
            reset = data.get('reset')
            if reset:
                return json.dumps({'status': 9})
        if data:
            set_data = {'$set': json.loads(request.data.decode())}
        else:
            return json.dumps({'status': 3})
        if device_name is not None:
            mongo.db['device_current'].update_one({'device_name': device_name}, set_data)
            return json.dumps({'status': 0})
        return json.dumps({'status': 1})

    def delete(self, item_id):
        pass


device_view = DeviceAPI.as_view('device_api')
api.add_url_rule('/device/', defaults={'device_name': None}, view_func=device_view, methods=['GET', ])
api.add_url_rule('/device/', view_func=device_view, methods=['POST', ])
api.add_url_rule('/device/<device_name>', view_func=device_view, methods=['GET', 'PUT', 'POST'])
