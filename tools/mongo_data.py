class device_default():
    documents = [{'device_name': 'host',
                  'switch': True,
                  'time_on': 0,
                  'time_off': 0,
                  'wifi_name': '',
                  'wifi_key': '',
                  'wifi_method': 1,
                  'ip_address': '192.168.1.191'
                  },
                 {'device_name': 'fan',
                  'switch': True,
                  'mode': 1,
                  'speed': 1
                  },
                 {'device_name': 'oled',
                  'switch': True,
                  'time': 120
                  },
                 {'device_name': 'thermometer',
                  'switch': True,
                  'temperature': 0,
                  'humidity': 0
                  },
                 {'device_name': 'pm25',
                  'switch': True,
                  'pm25': 0,
                  'pm10': 0,
                  'outdoor_air': 0
                  }
                 ]


class user_default():
    documents = [{'username': 'aircleaner',
                  'password': 'pbkdf2:sha256:50000$Xep1Q66v$20c93adb7c7086d400303045190758d7c72896a53f5e34a1d32638828fd0443b'}
                 ]

# debug
# import sys
# print(sys.path)