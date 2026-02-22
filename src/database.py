import os
import bcrypt
import uuid
import time

from fastapi import HTTPException
from pymongo import MongoClient
from src import models as Models
from src import MOCKUP_OBJECTS as Mockups
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client["carbon_db"]
users_table = db["users"]
collections_table = db["collections"]
cards_table = db["cards"]
favorites_table = db["favorites"]


def startup():
    if users_table.count_documents({}) == 0:
        users_table.insert_one(Mockups.user.model_dump())
        collections_table.insert_one(Mockups.collection.model_dump())
        cards_table.insert_one(Mockups.card.model_dump())

def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}

def create_user(name: str, email: str, password: str):
    try:
        user_id = uuid.uuid4()
        user = Models.User(
            userId=user_id,
            name=name,
            email=email,
            pass_hash=bcrypt.hashpw(bytes(password), bcrypt.gensalt()),
            createdAt=int(time.time())
        )
        users_table.insert_one(user.model_dump_json())
    except:
        raise HTTPException(status_code=400)

def read_user_by_email(email: str):
    try:
        res = users_table.find_one({"email": email}, {"_id": 0, "pass_hash": 0})
        return res
    except:
        raise HTTPException(status_code=500)

def read_user_by_user_id(user_id: str):
    try:
        res = users_table.find_one({"userId": user_id}, {"_id": 0})
        return res
    except:
        raise HTTPException(status_code=500)

def read_user_by_name(name: str):
    try:
        print(name)
        res = users_table.find_one({"name": name}, {"_id": 0, "pass_hash": 0})
        return res
    except:
        raise HTTPException(status_code=500)

def update_user(user_id: str, name: str, email: str, password: str):
    try:
        user = Models.User(
            userId=user_id,
            name=name,
            email=email,
            pass_hash=bcrypt.hashpw(bytes(password), bcrypt.gensalt()),
            createdAt=int(time.time())
        )
        users_table.find_one_and_update({"userId": user_id}, user)
    except:
        raise HTTPException(status_code=500)

def delete_user(user_id: str):
    try:
        users_table.find_one_and_delete({"userId": user_id})
    except:
        raise HTTPException(status_code=500)

def create_collection(user_id: str, title: str, description: str, color: Models.Color, public: bool):
    try:
        collection_id = uuid.uuid4()
        collection = Models.Collection(
            userId=user_id,
            collectionId=collection_id,
            title=title,
            description=description,
            color=color,
            public=public,
            createdAt=int(time.time())
        )
        collections_table.insert_one(collection.model_dump_json())
    except:
        raise HTTPException(status_code=400)

def read_collection(collection_id: str):
    try:
        res = collections_table.find_one({"collectionId": collection_id}, {"_id": 0})
        return res
    except:
        raise HTTPException(status_code=500)

def update_collection(user_id: str, collection_id: str, title: str, description: str, color: Models.Color, public: bool):
    try:
        collection = Models.Collection(
            userId=user_id,
            collectionId=collection_id,
            title=title,
            description=description,
            color=color,
            public=public,
            createdAt=int(time.time())
        )
        collections_table.find_one_and_update({"collectionId": collection_id}, collection.model_dump_json())
    except:
        raise HTTPException(status_code=400)

def delete_collection(collection_id: str):
    try:
        collections_table.find_one_and_delete({"collectionId": collection_id})
    except:
        raise HTTPException(status_code=500)

def create_card(collection_id: str, front: str, back: str, notes: str):
    try:
        card_id = uuid.uuid4()
        card = Models.Card(
            collectionId=collection_id,
            cardId=card_id,
            front=front,
            back=back,
            notes=notes,
            createdAt=int(time.time())
        )
        cards_table.insert_one(card.model_dump_json())
    except:
        raise HTTPException(status_code=400)

def read_card(card_id: str):
    try:
        res = cards_table.find_one({"cardId": card_id}, {"_id": 0})
        return res
    except:
        raise HTTPException(status_code=500)

def read_cards_from_collection(collection_id: str):
    try:
        res = cards_table.find({"collectionId": collection_id}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def update_card(collection_id: str, card_id: str, front: str, back: str, notes: str):
    try:
        card = Models.Card(
            collectionId=collection_id,
            cardId=card_id,
            front=front,
            back=back,
            notes=notes,
            createdAt=int(time.time())
        )
        cards_table.find_one_and_update({"cardId": card_id}, card.model_dump_json())
    except:
        raise HTTPException(status_code=400)

def delete_card(card_id: str):
    try:
        cards_table.find_one_and_delete({"cardId": card_id})
    except:
        raise HTTPException(status_code=500)

def create_favorite(user_id: str, collection_id: str):
    try:
        favorite_id = uuid.uuid4()
        favorite = Models.Favorite(
            userId=user_id,
            collection_id=collection_id,
            favoriteId=favorite_id,
            createdAt=int(time.time())
        )
        favorites_table.insert_one(favorite)
    except:
        raise HTTPException(status_code=400)
    return

def read_favorites(user_id: str):
    try:
        res = favorites_table.find({"userId": user_id}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def update_favorite(user_id: str, collection_id: str, favorite_id: str):
    try:
        favorite = Models.Favorite(
            userId=user_id,
            collectionId=collection_id,
            favoriteId=favorite_id,
            createdAt=int(time.time())
        )
        favorites_table.find_one_and_update({"favoriteId": favorite_id}, favorite)
    except:
        raise HTTPException(status_code=500)

def delete_favorite(favorite_id: str):
    try:
        favorites_table.find_one_and_delete({"favoriteId": favorite_id})
    except:
        raise HTTPException(status_code=500)
