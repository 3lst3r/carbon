from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.parse import unquote

from src import MOCKUP
from src import authentication
from src import cards
from src import categories
from src import collections
from src import database
from src import users

app = FastAPI()


@app.on_event("startup")
def startup_event():
    database.startup()
    return

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return database.health()

@app.get("/api/users")
def get_users():
    return MOCKUP.GET_ALL_USERS

@app.get("/api/user_by_email/{email}", status_code=200)
def get_user_by_email(email: str):
    return database.read_user_by_email(email=unquote(email))

@app.get("/api/user/{name}")
def get_user_by_name(name: str):
    return database.read_user_by_name(name=name)

@app.post("/api/user")
def post_user(user_id: str):
    return MOCKUP.POST_USER

@app.put("/api/user/{user}")
def put_user(user: str):
    return MOCKUP.PUT_USER

@app.delete("/api/user/{user}")
def delete_user(user: str):
    return MOCKUP.DELETE_USER

@app.get("/api/collections")
def get_collections():
    return MOCKUP.GET_ALL_COLLECTIONS

@app.get("/api/collection/{collection_id}")
def get_collection(collection_id: str):
    return database.read_collection(collection_id=collection_id)

@app.put("/api/collection/{collection}")
def put_collection(collection: str):
    return MOCKUP.GET_PUT_COLLECTION

@app.delete("/api/collection/{collection}")
def delete_collection(collection: str):
    return MOCKUP.DELETE_COLLECTION

@app.get("/api/cards")
def get_cards():
    return MOCKUP.GET_ALL_CARDS

@app.get("/api/card/{card_id}")
def get_card(card_id: str):
    return database.read_card(card_id=card_id)

@app.put("/api/card/{card}")
def put_card(card: str):
    return MOCKUP.GET_PUT_CARD

@app.post("/api/card/{card}")
def post_cards(card: str):
    return MOCKUP.POST_CARDS

@app.delete("/api/card/{card}")
def delete_card(card: str):
    return MOCKUP.DELETE_CARD

@app.get("/api/categories")
def get_categories():
    return MOCKUP.GET_ALL_CATEGORIES

@app.post("/api/signup")
def post_signup():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/api/login")
def post_login():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/api/save/{collection}")
def post_save_collection(collection: str):
    return MOCKUP.POST_SAVE_COLLECTION

@app.get("/api/saved/{user_id}")
def get_save_collection(user_id: str):
    return database.read_favorites(user_id=user_id)


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
