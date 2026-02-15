from fastapi import FastAPI
from pymongo import MongoClient
import os
import uuid
import bcrypt

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client["carbon_db"]
users = db["users"]
collections = db["collections"]
cards = db["cards"]

app = FastAPI()


@app.on_event("startup")
def startup_event():
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


@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}

# get all users
@app.get("/users")
def get_items():
    req = list(users.find({}, {"_id": 0}))
    return req

# get all collections
@app.get("/collections")
def get_collections():
    req = list(collections.find({}, {"_id": 0}))
    return req

# get all cards
@app.get("/cards")
def get_cards():
    req = list(cards.find({}, {"_id": 0}))
    return req

# TODO: create, update, delete
# get profile from {user}, including all collections
@app.get("/user/{user}")
def get_user(user: str):
    return {
        "user_id": "",
        "user_name": user,
        "collections": []
    }

# TODO: create, update, delete
# get {collection} from {user}, including all cards
@app.get("/user/{user}/collection/{collection}")
def get_collection(user: str, collection: str):
    return {
        "user_id": "",
        "user_name": user,
        "collection_id": "",
        "collection_name": collection,
        "cards": []
    }

# TODO: create, update, delete Card


# GET all users (locked)
# GET user by name
# GET user by user_id
# POST user
# PUT user
# DELETE user

# GET all collections (locked)
# GET collection by collection_id
# POST collection by user_id
# PUT collection by collection_id
# DELETE collection by collection_id

# GET all cards (locked)
# GET card by card_id
# POST card by collection_id
# PUT card by card_id
# DELETE card by card_id

# GET all categories

# POST signup
# POST login
# DELETE login

# GET health
# startup

# GET all public collections?
# POST save collection?
# GET all saved collections?
