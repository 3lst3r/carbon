import pytest
import mongomock
from unittest.mock import patch
from fastapi.testclient import TestClient
from src import MOCKUP_OBJECTS

@pytest.fixture(scope="function")
def mock_collections():
    mongo_client = mongomock.MongoClient()
    db = mongo_client["carbon_db"]
    return {
        "db": db,
        "users": db["users"],
        "collections": db["collections"],
        "cards": db["cards"],
        "favorites": db["favorites"]
    }

@pytest.fixture(scope="function")
def client(mock_collections: dict):
    with (
        patch("src.database.db", mock_collections["db"]),
        patch("src.database.users_table", mock_collections["users"]),
        patch("src.database.collections_table", mock_collections["collections"]),
        patch("src.database.cards_table", mock_collections["cards"]),
        patch("src.database.favorites_table", mock_collections["favorites"]),
    ):
        from src.main import app
        yield TestClient(app), mock_collections

ALICE = MOCKUP_OBJECTS.user_alice
BOB = MOCKUP_OBJECTS.user_bob

ALICE_PUBLIC = {
    "userId": ALICE.userId,
    "name": ALICE.email,
    "email": ALICE.email,
    "createdAt": ALICE.createdAt
}

class TestGetUsers:
    def test_returns_empty_list_when_no_users(self, client):
        test_client, _ = client
        response = test_client.get("/api/users")
        assert response.status_code == 200
        assert response.json() == []