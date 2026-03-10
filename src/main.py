from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.parse import unquote

from src import models
from src import MOCKUP
from src import database

app = FastAPI()


@app.on_event("startup")
def startup_event():
    database.startup()
    return

@app.get("/", status_code=200)
def root():
    return RedirectResponse(url="/docs")

@app.get("/health", status_code=200)
def health():
    return database.health()

@app.get("/api/users", status_code=200)
def get_users():
    return database.get_all_users()

@app.get("/api/user_by_email/{email}", status_code=200)
def get_user_by_email(email: str):
    return database.read_user_by_email(email=unquote(email))

@app.get("/api/user/{name}", status_code=200)
def get_user_by_name(name: str):
    return database.read_user_by_name(name=name)

@app.post("/api/user", status_code=201)
async def post_user(user: models.PostUser):
    return database.create_user(name=user.name, email=user.email, password=user.password)

@app.put("/api/user", status_code=201)
def put_user(user: models.PutUser):
    return database.update_user(user_id=user.userId, name=user.name, email=user.email, password=user.password)

@app.delete("/api/user/{user_id}", status_code=200)
def delete_user(user_id: str):
    return database.delete_user(user_id)

@app.get("/api/collections", status_code=200)
def get_collections():
    return database.get_all_collections()

@app.get("/api/collection/{collection_id}", status_code=200)
def get_collection(collection_id: str):
    return database.read_collection(collection_id=collection_id)

@app.put("/api/collection", status_code=201)
def put_collection(collection: models.PutCollection):
    return database.update_collection(collection_id=collection.collectionId, title=collection.title, description=collection.description, color=collection.color, public=collection.public)

@app.delete("/api/collection/{collection_id}", status_code=200)
def delete_collection(collection_id: str):
    return database.delete_collection(collection_id=collection_id)

@app.get("/api/cards", status_code=200)
def get_cards():
    return database.get_all_cards()

@app.get("/api/card/{card_id}", status_code=200)
def get_card(card_id: str):
    return database.read_card(card_id=card_id)

@app.put("/api/card", status_code=201)
def put_card(card: models.PutCard):
    return database.update_card(card_id=card.cardId, front=card.front, back=card.back, notes=card.notes)

@app.post("/api/card", status_code=201)
def post_cards(cards: list[models.PostCard]):
    return database.create_cards(cards)

@app.delete("/api/card/{card_id}", status_code=200)
def delete_card(card_id: str):
    return database.delete_card(card_id=card_id)

@app.get("/api/categories", status_code=200)
def get_categories():
    return MOCKUP.GET_ALL_CATEGORIES

@app.post("/api/signup", status_code=201)
def post_signup():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/api/login", status_code=201)
def post_login():
    return MOCKUP.POST_SIGNUP_LOGIN

@app.post("/api/save", status_code=201)
def post_save_collection(favorite: models.PostFavorite):
    database.create_favorite(user_id=favorite.userId, collection_id=favorite.collectionId)

@app.get("/api/saved", status_code=200)
def get_save_collection():
    return database.get_all_favorites()

@app.get("/api/saved/{user_id}", status_code=200)
def get_save_collection(user_id: str):
    return database.read_favorites(user_id=user_id)

@app.delete("/api/saved/{favorite_id}", status_code=200)
def get_save_collection(favorite_id: str):
    return database.delete_favorite(favorite_id=favorite_id)


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
