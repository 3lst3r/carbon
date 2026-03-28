import bcrypt
import uuid
import time

from fastapi import HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from src import models as Models
from src import MOCKUP_OBJECTS as Mockups
from src import config

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

client = MongoClient(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}")
db = client["carbon_db"]
users_table = db["users"]
collections_table = db["collections"]
cards_table = db["cards"]
favorites_table = db["favorites"]
categories_table = db["categories"]

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)

def startup():
    if categories_table.count_documents({}) == 0:
        initialize_categories()
    if config.WIPE_DATABASE_ON_RESTART:
        users_table.delete_many({})
        collections_table.delete_many({})
        cards_table.delete_many({})
        favorites_table.delete_many({})
        categories_table.delete_many({})
        initialize_categories()
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

def initialize_categories():
    categories_table.insert_one(Mockups.category_1.model_dump())
    categories_table.insert_one(Mockups.category_2.model_dump())
    categories_table.insert_one(Mockups.category_3.model_dump())
    categories_table.insert_one(Mockups.category_4.model_dump())
    categories_table.insert_one(Mockups.category_5.model_dump())
    categories_table.insert_one(Mockups.category_6.model_dump())
    categories_table.insert_one(Mockups.category_7.model_dump())
    categories_table.insert_one(Mockups.category_8.model_dump())
    categories_table.insert_one(Mockups.category_9.model_dump())
    categories_table.insert_one(Mockups.category_10.model_dump())

def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}

def get_all_users():
    try:
        res = list(users_table.find({}, {"_id": 0, "pass_hash": 0}))
        return res
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def create_user(name: str, email: str, password: str):
    res = users_table.find_one({"name": name})
    if res is not None:
        raise HTTPException(status_code=409)
    user_id = str(uuid.uuid4())
    user = Models.User(
        userId=user_id,
        name=name,
        email=email,
        pass_hash=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
        createdAt=int(time.time())
    )
    users_table.insert_one(user.model_dump())


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
    except TypeError:
        raise HTTPException(status_code=404)

def read_user_by_user_id(user_id: str):
    try:
        res = users_table.find_one({"userId": user_id}, {"_id": 0, "pass_hash": 0})
        return {
            "userId": res["userId"],
            "name": res["name"],
            "email": res["email"],
            "createdAt": res["createdAt"],
            "collections": get_collections_from_user_id(res["userId"])
        }
    except TypeError:
        raise HTTPException(status_code=404)

def read_user_by_user_id_raw(user_id: str):
    try:
        res = users_table.find_one({"userId": user_id}, {"_id": 0})
        return {
            "userId": res["userId"],
            "name": res["name"],
            "email": res["email"],
            "createdAt": res["createdAt"]
        }
    except TypeError:
        raise HTTPException(status_code=404)

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
    except TypeError:
        raise HTTPException(status_code=404)

def update_user(user_id: str, name: str, email: str, password: str):
    res = users_table.find_one_and_update(
        {"userId": user_id}, 
        {
            "$set": {
                **({"name": name} if name is not None else {}),
                **({"email": email} if email is not None else {}),
                **({"pass_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())} if password is not None else {})
            }
        }
    )
    if res is None:
        raise HTTPException(status_code=404)

def delete_user(user_id: str):
    res =users_table.find_one_and_delete({"userId": user_id})
    if res is None:
        raise HTTPException(status_code=404)

def get_all_collections():
    try:
        res = list(collections_table.find({}, {"_id": 0}))
        temp = []
        for element in res:
            temp.append({
            "user": read_user_by_user_id_raw(element["userId"]),
            "collectionId": element["collectionId"],
            "title": element["title"],
            "description": element["description"],
            "color": element["color"],
            "public": element["public"],
            "createdAt": element["createdAt"],
            "categories": element["categories"],
            "cards": read_cards_from_collection(element["collectionId"])
        })
        return temp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def get_collections_from_query(query: str):
    try:
        res = list(collections_table.find({"title": {"$regex": query}}, {"_id": 0}))
        temp = []
        for element in res:
            temp.append({
            "user": read_user_by_user_id_raw(element["userId"]),
            "collectionId": element["collectionId"],
            "title": element["title"],
            "description": element["description"],
            "color": element["color"],
            "public": element["public"],
            "createdAt": element["createdAt"],
            "categories": element["categories"],
            "cards": read_cards_from_collection(element["collectionId"])
        })
        return temp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def get_collections_from_category(category: str):
    try:
        res = list(collections_table.find({"categories.label": {"$regex": category, "$options": "i"}}, {"_id": 0}))
        temp = []
        for element in res:
            temp.append({
            "user": read_user_by_user_id_raw(element["userId"]),
            "collectionId": element["collectionId"],
            "title": element["title"],
            "description": element["description"],
            "color": element["color"],
            "public": element["public"],
            "createdAt": element["createdAt"],
            "categories": element["categories"],
            "cards": read_cards_from_collection(element["collectionId"])
        })
        return temp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def get_collections_from_user_id(user_id: str):
    try:
        res = list(collections_table.find({"userId": user_id}, {"_id": 0}))
        temp = []
        for element in res:
            temp.append({
            "user": read_user_by_user_id_raw(element["userId"]),
            "collectionId": element["collectionId"],
            "title": element["title"],
            "description": element["description"],
            "color": element["color"],
            "public": element["public"],
            "createdAt": element["createdAt"],
            "categories": element["categories"],
            "cards": read_cards_from_collection(element["collectionId"])
        })
        return temp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def create_collection(user_id: str, title: str, description: str, color: Models.Color, public: bool, categories: list[Models.Category]):
    try:
        collection_id = str(uuid.uuid4())
        collection = Models.Collection(
            userId=user_id,
            collectionId=collection_id,
            title=title,
            description=description,
            color=color,
            public=public,
            createdAt=int(time.time()),
            categories=categories
        )
        collections_table.insert_one(collection.model_dump())
        return read_collection(collection_id=collection_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)

def read_collection(collection_id: str):
    try:
        res = collections_table.find_one({"collectionId": collection_id}, {"_id": 0})
        return {
            "user": read_user_by_user_id_raw(res["userId"]),
            "collectionId": collection_id,
            "title": res["title"],
            "description": res["description"],
            "color": res["color"],
            "public": res["public"],
            "createdAt": res["createdAt"],
            "categories": res["categories"],
            "cards": read_cards_from_collection(collection_id)
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def update_collection(collection_id: str, title: str, description: str, color: Models.Color, public: bool, categories: list[Models.Category]):
    try:
        temp = []
        if categories is None:
            temp = None
        else:
            for element in categories:
                temp.append({
                    "label": element.label,
                    "value": element.value
                })
        collections_table.find_one_and_update(
            {"collectionId": collection_id}, 
            {
                "$set": {
                    **({"title": title} if title is not None else {}),
                    **({"description": description} if description is not None else {}),
                    **({"color": color} if color is not None else {}),
                    **({"public": public} if public is not None else {}),
                    **({"categories": temp} if temp is not None else {})
                }
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

def delete_collection(collection_id: str):
    try:
        collections_table.find_one_and_delete({"collectionId": collection_id})
    except:
        raise HTTPException(status_code=500)

def get_all_cards():
    try:
        res = list(cards_table.find({}, {"_id": 0}))
        return res
    except:
        raise HTTPException(status_code=500)

def create_cards(cards: Models.PostCards):
    try:
        for element in cards.cards:
            card_id = str(uuid.uuid4())
            card = Models.Card(
                collectionId=cards.collectionId,
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
        res = list(cards_table.find({"collectionId": collection_id}, {"_id": 0}))
        return res
    except:
        raise HTTPException(status_code=500)

def update_card(card_id: str, front: str, back: str, notes: str):
    try:
        cards_table.find_one_and_update(
            {"cardId": card_id}, 
            {
                "$set": {
                    **({"front": front} if front is not None else {}),
                    **({"back": back} if back is not None else {}),
                    **({"notes": notes} if notes is not None else {})
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
        res = list(favorites_table.find({}, {"_id": 0}))
        return res
    except:
        raise HTTPException(status_code=500)

def read_favorites(user_id: str):
    try:
        res = list(favorites_table.find({"userId": user_id}, {"_id": 0}))
        return res
    except:
        raise HTTPException(status_code=500)

def delete_favorite(favorite_id: str):
    try:
        favorites_table.find_one_and_delete({"favoriteId": favorite_id})
    except:
        raise HTTPException(status_code=500)

def get_all_categories():
    try:
        res = list(categories_table.find({}, {"_id": 0}))
        return res
    except:
        raise HTTPException(status_code=500)



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def signup(name: str, email: str, password: str, response: Response):
    create_user(name=name, email=email, password=password)
    return login(email=email, password=password, response=response)

def login(email: str, password: str, response: Response):
    res = users_table.find_one({"email": email}, {"_id": 0})
    if not res:
        return {"msg": "credentials unmatching"}
    if bcrypt.checkpw(password.encode("utf-8"), res["pass_hash"]):
        token = create_access_token({
            "sub": res["email"],
            "userId": str(res["userId"])
        })
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return {
            "name": res["name"],
            "email": res["email"],
            "userId": str(res["userId"])
        }
    return {"msg": "credentials unmatching"}

def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"msg": "logged out"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = users_table.find_one({"email": user_email}, {"_id": 0, "pass_hash": 0})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# def get_current_user_optional(token: str = Depends(oauth2_scheme)):
#     if token is None:
#         return False
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_email = payload.get("sub")
#         if user_email is None:
#             raise HTTPException(status_code=500, detail="token contains no field 'email'")
#     except JWTError:
#         raise HTTPException(status_code=500, detail="a JWTError occured")

#     user = users_table.find_one({"email": user_email}, {"_id": 0, "pass_hash": 0, "createdAt": 0})
#     if user is None:
#         raise HTTPException(status_code=500, detail="user not found in database")

#     return user

from fastapi import Cookie

def get_current_user_optional(access_token: str | None = Cookie(default=None)):
    if access_token is None:
        return False
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=500, detail="token contains no field 'email'")
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=500, detail="a JWTError occured")

    user = users_table.find_one({"email": user_email}, {"_id": 0, "pass_hash": 0, "createdAt": 0})
    if user is None:
        raise HTTPException(status_code=500, detail="user not found in database")

    return user