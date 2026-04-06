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

class TestHealth:
    def test_get_health(self, test_client: TestClient):
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "database": "up",
            "status": "ok"
        }

class TestGetAllCategories:
    def test_get_all_categories(self, test_client: TestClient):
        response = test_client.get("/api/categories")
        assert response.status_code == 200
        assert type(response.json()) == type([])
        assert len(response.json()) == 10
        assert "label" in response.json()[0]
        assert "value" in response.json()[0]