from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.vietnamesehtr
image_db = db.image
user_db = db.user