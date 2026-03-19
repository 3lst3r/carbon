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

@pytest.fixture(scope="function")
def test_client(client) -> TestClient:
    http_client, _ = client
    return http_client

ALICE = MOCKUP_OBJECTS.user_alice
BOB = MOCKUP_OBJECTS.user_bob
CARL = {
    "name": "Carl",
    "email": "carl@example.com",
    "password": "carl123"
}

ALICE_PUBLIC = {
    "userId": ALICE.userId,
    "name": ALICE.email,
    "email": ALICE.email,
    "createdAt": ALICE.createdAt
}

class TestGetUsers:
    # empty user list
    def test_empty_user_list(self, test_client: TestClient):
        response = test_client.get("/api/users")
        assert response.status_code == 200
        assert response.json() == []
    
    # filled user list
    def test_filled_user_list(self, test_client: TestClient):
        test_client.post("/api/user", json=CARL)
        response = test_client.get("/api/users")
        assert response.status_code == 200
    
    # get user by name
    def test(self, test_client: TestClient):
        test_client.post("/api/user", json=CARL)
        response = test_client.get(f"/api/user/{CARL["name"]}")
        assert response.status_code == 200
    
    # get user by email
    def test(self, test_client: TestClient):
        test_client.post("/api/user", json=CARL)
        return

class TestPostUsers:
    # new user
    def test_new_user(self, test_client: TestClient):
        response = test_client.post("/api/signup", json=CARL)
        assert response.status_code == 201
    
    # error existing user
    def test_error_existing_user(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        response = test_client.post("/api/signup", json=CARL)
        assert response.status_code == 409
    
    # error incomplete user
    def test_error_incomplete_user(self, test_client: TestClient):
        response = test_client.post("/api/signup", json={"name": "Carl"})
        assert response.status_code == 400

class TestPutUsers:
    # update user
    def test(self, test_client: TestClient):
        return
    
    # error not existing user
    def test(self, test_client: TestClient):
        return
    
    # error incomplete user
    def test(self, test_client: TestClient):
        return

class TestDeleteUsers:
    # delete user
    def test(self, test_client: TestClient):
        return
    
    # error not existing user
    def test(self, test_client: TestClient):
        return
