
from pymongo import MongoClient
import os
import bcrypt
import uuid

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client["carbon_db"]
users = db["users"]
collections = db["collections"]
cards = db["cards"]


def startup():
    if users.count_documents({}) == 0:
        user_id = str(uuid.uuid4())
        collection_id = str(uuid.uuid4())
        card_id = str(uuid.uuid4())
        users.insert_one({
            "user_id": user_id,
            "name": "test_user",
            "pass_hash": bcrypt.hashpw(b"password", bcrypt.gensalt())
        })
        collections.insert_one({
            "user_id": user_id,
            "collection_id": collection_id,
            "title": "this is the title of the collection",
            "description": "this is the description of the collection",
            "color": "FFFFFF"
        })
        cards.insert_one({
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