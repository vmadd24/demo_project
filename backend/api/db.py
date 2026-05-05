from django.conf import settings
from pymongo import MongoClient

_client = MongoClient(settings.MONGO_URL)
db = _client[settings.MONGO_DB_NAME]

users = db["users"]
products = db["products"]
orders = db["orders"]
