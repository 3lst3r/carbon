from pydantic import BaseModel
from enum import Enum

class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"
    orange = "orange"
    purple = "purple"

class User(BaseModel):
    userId: str
    name: str
    email: str
    pass_hash: bytes
    createdAt: int

class Collection(BaseModel):
    userId: str
    collectionId: str
    title: str
    description: str
    color: Color
    public: bool
    createdAt: int

class Card(BaseModel):
    collectionId: str
    cardId: str
    front: str
    back: str
    notes: str
    createdAt: int

class Favorite(BaseModel):
    userId: str
    collectionId: str
    favoriteId: str
    createdAt: str



class PostUser(BaseModel):
    name: str
    email: str
    password: str

class PutUser(BaseModel):
    userId: str
    name: str
    email: str
    password: str