from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"
    orange = "orange"
    purple = "purple"

class Category(BaseModel):
    label: str
    value: str

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
    categories: list[Category]

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
    createdAt: int



class PostUser(BaseModel):
    name: str
    email: str
    password: str

class PutUser(BaseModel):
    userId: str
    name: str
    email: str
    password: str

class PostCollection(BaseModel):
    userId: str
    title: str
    description: str = ""
    color: Color = "blue"
    public: bool = False
    categories: list[Category] = Field(default_factory=list)

class PutCollection(BaseModel):
    collectionId: str
    title: str
    description: str
    color: Color
    public: bool
    categories: list[Category]

class PutCard(BaseModel):
    cardId: str
    front: str
    back: str
    notes: str


class PostCard(BaseModel):
    front: str
    back: str
    notes: str

class PostCards(BaseModel):
    collectionId: str
    cards: list[PostCard]

class PostFavorite(BaseModel):
    userId: str
    collectionId: str

class PostLogin(BaseModel):
    email: str
    password: str

