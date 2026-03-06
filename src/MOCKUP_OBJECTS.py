import time
import bcrypt
from src import models as Models

user_id = "example-userid-alice"
collection_id = "example-collectionid-alice"
card_id = "example-cardid-alice"
user = Models.User(
    userId=user_id,
    name="Alice",
    email="alice@example.com",
    pass_hash=bcrypt.hashpw(bytes(b"password123"), bcrypt.gensalt()),
    createdAt=int(time.time())
)
collection = Models.Collection(
    userId=user_id,
    collectionId=collection_id,
    title="Test Title",
    description="Test Description",
    color="red",
    public=True,
    createdAt=int(time.time())
)
card = Models.Card(
    collectionId=collection_id,
    cardId=card_id,
    front="Test Front",
    back="Test Back",
    notes="Test Notes",
    createdAt=int(time.time())
)