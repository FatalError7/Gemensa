from pymongo import MongoClient
import bcrypt
import uuid

client = MongoClient("mongodb://localhost:27017/")
db = client["Gemensa"]
user = db["User"]

hashed = bcrypt.hashpw('1234'.encode(
    'utf-8'), bcrypt.gensalt())
user.insert_one({
    "_id": uuid.uuid4().hex,
    "username": 'admin',
    "password": hashed,
    "nome": 'Admin',
    "isMensa": "false",
    "isAdmin" : "true"
})

user.insert_one({
    "_id": uuid.uuid4().hex,
    "username": 'mensa',
    "password": hashed,
    "nome": 'Admin',
    "isMensa": "true",
    "isAdmin" : "false"
})
