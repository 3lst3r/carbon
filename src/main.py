from fastapi import FastAPI
from pymongo import MongoClient
import os
import uuid
import bcrypt
from src import MOCKUP

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
    # if users.count_documents({}) == 0:
    #     user_id = str(uuid.uuid4())
    #     collection_id = str(uuid.uuid4())
    #     card_id = str(uuid.uuid4())
    #     users.insert_one({
    #         "user_id": user_id,
    #         "name": "test_user",
    #         "pass_hash": bcrypt.hashpw(b"password", bcrypt.gensalt())
    #     })
    #     collections.insert_one({
    #         "user_id": user_id,
    #         "collection_id": collection_id,
    #         "title": "this is the title of the collection",
    #         "description": "this is the description of the collection",
    #         "color": "FFFFFF"
    #     })
    #     cards.insert_one({
    #         "collection_id": collection_id,
    #         "card_id": card_id,
    #         "front": "this is the front side",
    #         "back": "this is the back side"
    #     })
    return


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

@app.get("/users")
def get_users():
    return MOCKUP.GET_ALL_USERS

@app.get("/user/{user}")
def get_user(user: str):
    return MOCKUP.GET_USER

@app.post("/user/{user}")
def post_user(user: str):
    return MOCKUP.POST_USER

@app.put("/user/{user}")
def put_user(user: str):
    return MOCKUP.PUT_USER

@app.delete("/user/{user}")
def delete_user(user: str):
    return MOCKUP.DELETE_USER

@app.get("/collections")
def get_collections():
    return MOCKUP.GET_ALL_COLLECTIONS

@app.get("/collection/{collection}")
def get_collection(collection: str):
    return MOCKUP.GET_PUT_COLLECTION

@app.put("/collection/{collection}")
def put_collection(collection: str):
    return MOCKUP.GET_PUT_COLLECTION

@app.delete("/collection/{collection}")
def delete_collection(collection: str):
    return MOCKUP.DELETE_COLLECTION

@app.get("/cards")
def get_cards():
    return MOCKUP.GET_ALL_CARDS

@app.get("/card/{card}")
def get_card(card: str):
    return MOCKUP.GET_PUT_CARD

@app.put("/card/{card}")
def put_card(card: str):
    return MOCKUP.GET_PUT_CARD

@app.post("/card/{card}")
def post_cards(card: str):
    return MOCKUP.POST_CARDS

@app.delete("/card/{card}")
def delete_card(card: str):
    return MOCKUP.DELETE_CARD

@app.get("/categories")
def get_categories():
    return MOCKUP.GET_ALL_CATEGORIES

@app.post("/signup")
def post_signup():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/login")
def post_login():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/save/{collection}")
def post_save_collection(collection: str):
    return MOCKUP.POST_SAVE_COLLECTION

@app.get("/saved")
def post_save_collection():
    return MOCKUP.GET_SAVED_COLLECTIONS

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

# POST save collection?
# GET all saved collections?
