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