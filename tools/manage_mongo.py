__author__ = 'ASH975'

from pymongo import MongoClient
from tools.mongo_data import device_default, user_default


client = MongoClient('127.0.0.1', 27017)
db_aircleaner = client.aircleaner
collection_device_default = db_aircleaner.device_default
collection_device_current = db_aircleaner.device_current
collection_user_default = db_aircleaner.user_default
collection_user_current = db_aircleaner.user_current

collection_device_default.insert_many(device_default.documents)
