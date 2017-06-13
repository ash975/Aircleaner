import tools.mongo_management

cursor = tools.mongo_management.collection_device_current.find()
items = {}
for item in cursor:
     items.update({item['device_name']: item})

print(items)