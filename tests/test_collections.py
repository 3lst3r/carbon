import pytest
from fastapi.testclient import TestClient
from src import MOCKUP_OBJECTS

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

def create_user_and_get_user_id(test_client: TestClient):
    test_client.post("/api/signup", json=CARL)
    return test_client.get("/api/user_by_name/Carl").json()["userId"]

class TestGetAllCollections:
    # empty collection list
    def test_empty_collection_list(self, test_client: TestClient):
        response = test_client.get("/api/collections")
        assert response.status_code == 200
        assert response.json() == []
    
    # filled collection list
    def test_filled_collection_list(self, test_client: TestClient):
        user_id = create_user_and_get_user_id(test_client=test_client)
        test_client.post("/api/collection", json={
            "userId": user_id,
            "title": "Title"
        })
        response = test_client.get("/api/collections")
        assert response.status_code == 200
        assert response.json() is not None