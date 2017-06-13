from flask import json
from flask import current_app, session
from bson import json_util
from bson import ObjectId


def bson_to_json(data):
    return json.dumps(data, default=json_util.default)


def bson_obj_id(id):
    return ObjectId(id)


def pm_color_class(pm, base_class):
    pm = int(pm)
    color = ''
    if pm > 150:
        color = base_class+' btn-danger'
    elif pm > 100:
        color = base_class+' btn-warning'
    elif pm > 50:
        color = base_class+' btn-info'
    elif pm >= 0:
        color = base_class+' btn-success'
    return color


def temp_color_class(temperature):
    color = ''
    temperature = int(temperature)
    if temperature > 35:
        color = 'my-circle btn-danger'
    elif temperature > 26:
        color = 'my-circle btn-warning'
    elif temperature > 18:
        color = 'my-circle btn-success'
    elif temperature > 5:
        color = 'my-circle btn-info'
    else:
        color = 'my-circle btn-primary'
    return color
