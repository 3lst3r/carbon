import bcrypt
import uuid
import time

from fastapi import HTTPException
from pymongo import MongoClient
from src import models as Models
from src import MOCKUP_OBJECTS as Mockups
from src import config

client = MongoClient(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}")
db = client["carbon_db"]
users_table = db["users"]
collections_table = db["collections"]
cards_table = db["cards"]
favorites_table = db["favorites"]


def startup():
    if config.WIPE_DATABASE_ON_RESTART:
        users_table.delete_many({})
        collections_table.delete_many({})
        cards_table.delete_many({})
        favorites_table.delete_many({})
    if users_table.count_documents({}) == 0 and config.FILL_DATABASE_WITH_DEMO_DATA:
        users_table.insert_one(Mockups.user_alice.model_dump())
        users_table.insert_one(Mockups.user_bob.model_dump())
        collections_table.insert_one(Mockups.collection_1.model_dump())
        collections_table.insert_one(Mockups.collection_2.model_dump())
        collections_table.insert_one(Mockups.collection_3.model_dump())
        collections_table.insert_one(Mockups.collection_4.model_dump())
        cards_table.insert_one(Mockups.card_1.model_dump())
        cards_table.insert_one(Mockups.card_2.model_dump())
        cards_table.insert_one(Mockups.card_3.model_dump())
        cards_table.insert_one(Mockups.card_4.model_dump())
        cards_table.insert_one(Mockups.card_5.model_dump())
        cards_table.insert_one(Mockups.card_6.model_dump())
        cards_table.insert_one(Mockups.card_7.model_dump())
        cards_table.insert_one(Mockups.card_8.model_dump())
        favorites_table.insert_one(Mockups.favorite_alice_1.model_dump())
        favorites_table.insert_one(Mockups.favorite_bob_1.model_dump())
        favorites_table.insert_one(Mockups.favorite_bob_2.model_dump())

def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}

def get_all_users():
    try:
        res = users_table.find({}, {"_id": 0, "pass_hash": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def create_user(name: str, email: str, password: str):
    try:
        user_id = str(uuid.uuid4())
        user = Models.User(
            userId=user_id,
            name=name,
            email=email,
            pass_hash=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
            createdAt=int(time.time())
        )
        users_table.insert_one(user.model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)

def read_user_by_email(email: str):
    try:
        res = users_table.find_one({"email": email}, {"_id": 0, "pass_hash": 0})
        return {
            "userId": res["userId"],
            "name": res["name"],
            "email": res["email"],
            "createdAt": res["createdAt"],
            "collections": get_collections_from_user_id(res["userId"])
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def read_user_by_user_id(user_id: str):
    try:
        res = users_table.find_one({"userId": user_id}, {"_id": 0})
        return {
            "userId": res["userId"],
            "name": res["name"],
            "email": res["email"],
            "createdAt": res["createdAt"],
            "collections": get_collections_from_user_id(res["userId"])
        }
    except:
        raise HTTPException(status_code=500)

def read_user_by_name(name: str):
    try:
        res = users_table.find_one({"name": name}, {"_id": 0, "pass_hash": 0})
        return {
            "userId": res["userId"],
            "name": res["name"],
            "email": res["email"],
            "createdAt": res["createdAt"],
            "collections": get_collections_from_user_id(res["userId"])
        }
    except:
        raise HTTPException(status_code=500)

def update_user(user_id: str, name: str, email: str, password: str):
    try:
        users_table.find_one_and_update(
            {"userId": user_id}, 
            {
                "$set": {
                    "name": name,
                    "email": email,
                    "pass_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                }
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def delete_user(user_id: str):
    try:
        users_table.find_one_and_delete({"userId": user_id})
    except:
        raise HTTPException(status_code=500)

def get_all_collections():
    try:
        res = collections_table.find({}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def get_collections_from_user_id(user_id: str):
    try:
        res = collections_table.find({"userId": user_id}, {"_id": 0}).to_list()
        return res
    except Exception as e:
        print(e)
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
        return {
            "userId": res["userId"],
            "collectionId": collection_id,
            "title": res["title"],
            "description": res["description"],
            "color": res["color"],
            "public": res["public"],
            "createdAt": res["createdAt"],
            "cards": read_cards_from_collection(collection_id)
        }
    except:
        raise HTTPException(status_code=500)

def update_collection(collection_id: str, title: str, description: str, color: Models.Color, public: bool):
    try:
        collections_table.find_one_and_update(
            {"collectionId": collection_id}, 
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "color": color,
                    "public": public
                }
            }
        )
    except:
        raise HTTPException(status_code=500)

def delete_collection(collection_id: str):
    try:
        collections_table.find_one_and_delete({"collectionId": collection_id})
    except:
        raise HTTPException(status_code=500)

def get_all_cards():
    try:
        res = cards_table.find({}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def create_cards(cards: list[Models.PostCard]):
    try:
        for element in cards:
            card_id = str(uuid.uuid4())
            card = Models.Card(
                collectionId=element.collectionId,
                cardId=card_id,
                front=element.front,
                back=element.back,
                notes=element.notes,
                createdAt=int(time.time())
            )
            cards_table.insert_one(card.model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

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

def update_card(card_id: str, front: str, back: str, notes: str):
    try:
        cards_table.find_one_and_update(
            {"cardId": card_id}, 
            {
                "$set": {
                    "front": front,
                    "back": back,
                    "notes": notes
                }
            }
        )
    except:
        raise HTTPException(status_code=400)

def delete_card(card_id: str):
    try:
        cards_table.find_one_and_delete({"cardId": card_id})
    except:
        raise HTTPException(status_code=500)

def create_favorite(user_id: str, collection_id: str):
    try:
        favorite_id = str(uuid.uuid4())
        favorite = Models.Favorite(
            userId=user_id,
            collectionId=collection_id,
            favoriteId=favorite_id,
            createdAt=int(time.time())
        )
        favorites_table.insert_one(favorite.model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)
    return

def get_all_favorites():
    try:
        res = favorites_table.find({}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def read_favorites(user_id: str):
    try:
        res = favorites_table.find({"userId": user_id}, {"_id": 0}).to_list()
        return res
    except:
        raise HTTPException(status_code=500)

def delete_favorite(favorite_id: str):
    try:
        favorites_table.find_one_and_delete({"favoriteId": favorite_id})
    except:
        raise HTTPException(status_code=500)
