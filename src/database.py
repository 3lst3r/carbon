from pymongo import MongoClient
import os
import bcrypt
import uuid

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client["carbon_db"]
users_table = db["users"]
collections_table = db["collections"]
cards_table = db["cards"]
favorites = db["favorites"]


def startup():
    if users_table.count_documents({}) == 0:
        user_id = str(uuid.uuid4())
        collection_id = str(uuid.uuid4())
        card_id = str(uuid.uuid4())
        users_table.insert_one({
            "user_id": user_id,
            "name": "test_user",
            "pass_hash": bcrypt.hashpw(b"password", bcrypt.gensalt())
        })
        collections_table.insert_one({
            "user_id": user_id,
            "collection_id": collection_id,
            "title": "this is the title of the collection",
            "description": "this is the description of the collection",
            "color": "FFFFFF"
        })
        cards_table.insert_one({
            "collection_id": collection_id,
            "card_id": card_id,
            "front": "this is the front side",
            "back": "this is the back side"
        })

def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}

def insert_user(name: str, password: str):
    try:
        user_id = str(uuid.uuid4())
        users_table.insert_one({
            "userId": user_id,
            "name": name,
            "passHash": bcrypt.hashpw(bytes(password), bcrypt.gensalt())
        })
        return {
            "userId": user_id,
            "name": name
        }
    except Exception as e:
        print("An exception occured: ", e)
        return 500

def insert_collection(user_id: str, title: str, description: str, color: str):
    try:
        collection_id = str(uuid.uuid4())
        collections_table.insert_one({
            "userId": user_id,
            "collectionId": collection_id,
            "title": title,
            "description": description,
            "color": color
        })
        return {
            "userId": user_id,
            "collectionId": collection_id,
            "title": title,
            "description": description,
            "color": color,
            "totalCards": 0,
            "cards": []
        }
    except Exception as e:
        print("An exception occured: ", e)
        return 500

def insert_cards(cards: list):
    formatted = []
    for card in cards:
        temp = {
            "collectionId": card["collectionId"],
            "cardId": str(uuid.uuid4()),
            "front": card["front"],
            "back": card["back"]
        }
        formatted.append(temp)
    try:
        cards_table.insert_many(formatted)
        return formatted
    except Exception as e:
        print("An exception occured: ", e)
        return 500