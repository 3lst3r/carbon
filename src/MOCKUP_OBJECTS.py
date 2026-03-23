import time
import bcrypt
from src import models as Models

user_id_alice = "example-userid-alice"
user_id_bob = "example-userid-bob"

collection_id_alice_1 = "example-collectionid-alice-1"
collection_id_alice_2 = "example-collectionid-alice-2"
collection_id_bob_1 = "example-collectionid-bob-1"
collection_id_bob_2 = "example-collectionid-bob-2"

card_id_alice_1 = "example-cardid-alice-1"
card_id_alice_2 = "example-cardid-alice-2"
card_id_alice_3 = "example-cardid-alice-3"
card_id_alice_4 = "example-cardid-alice-4"
card_id_bob_1 = "example-cardid-bob-1"
card_id_bob_2 = "example-cardid-bob-2"
card_id_bob_3 = "example-cardid-bob-3"
card_id_bob_4 = "example-cardid-bob-4"

favorite_id_alice_1 = "example-favoriteid-alice-1"
favorite_id_bob_1 = "example-favoriteid-bob-1"
favorite_id_bob_2 = "example-favoriteid-bob-2"

creation_time = int(time.time())

user_alice = Models.User(
    userId=user_id_alice,
    name="Alice",
    email="alice@example.com",
    pass_hash=bcrypt.hashpw(bytes(b"alice123"), bcrypt.gensalt()),
    createdAt=creation_time
)
user_bob = Models.User(
    userId=user_id_bob,
    name="Bob",
    email="bob@example.com",
    pass_hash=bcrypt.hashpw(bytes(b"bob123"), bcrypt.gensalt()),
    createdAt=creation_time
)

category_1 = Models.Category(
    label="MATHEMATIK",
    value="Mathematik"
)
category_2 = Models.Category(
    label="DEUTSCH",
    value="Deutsch"
)

collection_1 = Models.Collection(
    userId=user_id_alice,
    collectionId=collection_id_alice_1,
    title="Test Title 1",
    description="Test Description 1",
    color="red",
    public=True,
    createdAt=creation_time,
    categories=[
        category_1
    ]
)
collection_2 = Models.Collection(
    userId=user_id_alice,
    collectionId=collection_id_alice_2,
    title="Test Title 2",
    description="Test Description 2",
    color="green",
    public=False,
    createdAt=creation_time,
    categories=[
        category_2
    ]
)
collection_3 = Models.Collection(
    userId=user_id_bob,
    collectionId=collection_id_bob_1,
    title="Test Title 3",
    description="Test Description 3",
    color="blue",
    public=True,
    createdAt=creation_time,
    categories=[
        category_1,
        category_2
    ]
)
collection_4 = Models.Collection(
    userId=user_id_bob,
    collectionId=collection_id_bob_2,
    title="Test Title 4",
    description="Test Description 4",
    color="orange",
    public=False,
    createdAt=creation_time,
    categories=[]
)

card_1 = Models.Card(
    collectionId=collection_id_alice_1,
    cardId=card_id_alice_1,
    front="Test Front 1",
    back="Test Back 1",
    notes="Test Notes 1",
    createdAt=creation_time
)
card_2 = Models.Card(
    collectionId=collection_id_alice_1,
    cardId=card_id_alice_2,
    front="Test Front 2",
    back="Test Back 2",
    notes="Test Notes 2",
    createdAt=creation_time
)
card_3 = Models.Card(
    collectionId=collection_id_alice_2,
    cardId=card_id_alice_3,
    front="Test Front 3",
    back="Test Back 3",
    notes="Test Notes 3",
    createdAt=creation_time
)
card_4 = Models.Card(
    collectionId=collection_id_alice_2,
    cardId=card_id_alice_4,
    front="Test Front 4",
    back="Test Back 4",
    notes="Test Notes 4",
    createdAt=creation_time
)
card_5 = Models.Card(
    collectionId=collection_id_bob_1,
    cardId=card_id_bob_1,
    front="Test Front 5",
    back="Test Back 5",
    notes="Test Notes 5",
    createdAt=creation_time
)
card_6 = Models.Card(
    collectionId=collection_id_bob_1,
    cardId=card_id_bob_2,
    front="Test Front 6",
    back="Test Back 6",
    notes="Test Notes 6",
    createdAt=creation_time
)
card_7 = Models.Card(
    collectionId=collection_id_bob_2,
    cardId=card_id_bob_3,
    front="Test Front 7",
    back="Test Back 7",
    notes="Test Notes 7",
    createdAt=creation_time
)
card_8 = Models.Card(
    collectionId=collection_id_bob_2,
    cardId=card_id_bob_4,
    front="Test Front 8",
    back="Test Back 8",
    notes="Test Notes 8",
    createdAt=creation_time
)

favorite_alice_1 = Models.Favorite(
    userId=user_id_alice,
    collectionId=collection_id_bob_1,
    favoriteId=favorite_id_alice_1,
    createdAt=creation_time
)
favorite_bob_1 = Models.Favorite(
    userId=user_id_bob,
    collectionId=collection_id_alice_1,
    favoriteId=favorite_id_bob_1,
    createdAt=creation_time
)
favorite_bob_2 = Models.Favorite(
    userId=user_id_bob,
    collectionId=collection_id_alice_2,
    favoriteId=favorite_id_bob_2,
    createdAt=creation_time
)
