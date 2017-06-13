import json
import requests

data = json.dumps({"switch": False})

data_mode = json.dumps({"mode": 2})

data_pm25 = json.dumps({"pm25": 23})

data_fan_switch = json.dumps({'switch': True})

print(type(data))

# r = requests.put('http://192.168.1.191/api/v1.0/device/fan', data=data_fan_switch)


r = requests.post('http://192.168.1.191/api/v1.0/device/pm25', data=data_pm25)

# r = requests.get('http://192.168.1.191/api/v1.0/device/fan')s

# print(type(json.loads(r.content.decode())))
