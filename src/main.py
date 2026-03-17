from fastapi import FastAPI, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from urllib.parse import unquote

from src import models
from src import database

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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

@app.put("/api/user", status_code=201)
def put_user(user: models.PutUser):
    return database.update_user(user_id=user.userId, name=user.name, email=user.email, password=user.password)

@app.delete("/api/user/{user_id}", status_code=200)
def delete_user(user_id: str):
    return database.delete_user(user_id)

@app.get("/api/collections", status_code=200)
def get_collections():
    return database.get_all_collections()

@app.get("/api/collections/popular", status_code=200)
def get_popular_collections():
    return database.get_all_collections()[:5]

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

@app.post("/api/save", status_code=201)
def post_save_collection(favorite: models.PostFavorite):
    database.create_favorite(user_id=favorite.userId, collection_id=favorite.collectionId)

@app.get("/api/saved", status_code=200)
def get_all_saved_collections():
    return database.get_all_favorites()

@app.get("/api/saved/{user_id}", status_code=200)
def get_saved_collection(user_id: str):
    return database.read_favorites(user_id=user_id)

@app.delete("/api/saved/{favorite_id}", status_code=200)
def delete_saved_collection(favorite_id: str):
    return database.delete_favorite(favorite_id=favorite_id)




@app.post("/api/signup", status_code=201)
async def signup(user: models.PostUser, response: Response):
    return database.signup(name=user.name, email=user.email, password=user.password, response=response)

@app.get("/api/login", status_code=200)
def get_login_info(current_user = Depends(database.get_current_user_optional)):
    return current_user

@app.post("/api/login", status_code=201)
async def login(user: models.PostLogin, response: Response):
    return database.login(email=user.email, password=user.password, response=response)

@app.post("/api/logout", status_code=201)
async def logout(response: Response):
    return database.logout(response=response)

@app.post("/api/token", status_code=200)
async def login_oauth(form_data: OAuth2PasswordRequestForm = Depends()):
    return database.login(email=form_data.username, password=form_data.password)

@app.get("/api/home", status_code=200)
def read_current_user(current_user: dict = Depends(database.get_current_user)):
    return database.read_user_by_user_id(current_user["userId"])