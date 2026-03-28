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
CARL_UPDATED = {
    "name": "Carl Updated",
    "email": "carl-updated@example.com",
    "password": "carl123updated"
}

ALICE_PUBLIC = {
    "userId": ALICE.userId,
    "name": ALICE.email,
    "email": ALICE.email,
    "createdAt": ALICE.createdAt
}

# GET /api/users
class TestGetAllUsers:
    # empty user list
    def test_empty_user_list(self, test_client: TestClient):
        response = test_client.get("/api/users")
        assert response.status_code == 200
        assert response.json() == []
    
    # filled user list
    def test_filled_user_list(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        response = test_client.get("/api/users")
        assert response.status_code == 200
        assert response.json() is not None

# GET /api/user/{userId}
class TestGetUserByUserId:
    # get user by id
    def test_get_existing_user_by_user_id(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        user_id = test_client.get("/api/users").json()[0]["userId"]
        response = test_client.get(f"/api/user/{user_id}")
        assert response.status_code == 200
        temp = response.json()
        assert temp["userId"] == user_id
        assert temp["name"] == CARL["name"]
        assert temp["email"] == CARL["email"]
        assert "password" not in temp
        assert "pass_hash" not in temp
        assert temp["createdAt"] is not None

    # error userId does not exist
    def test_get_error_by_false_user_id(self, test_client: TestClient):
        response = test_client.get("/api/user/false-user-id")
        assert response.status_code == 404

# GET /api/user_by_email/{email}
class TestGetUserByUserEmail:
    # get user by email
    def test_get_existing_user_by_user_id(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        response = test_client.get(f"/api/user_by_email/{CARL["email"]}")
        assert response.status_code == 200
        temp = response.json()
        assert temp["userId"] is not None
        assert temp["name"] == CARL["name"]
        assert temp["email"] == CARL["email"]
        assert "password" not in temp
        assert "pass_hash" not in temp
        assert temp["createdAt"] is not None

    # error email does not exist
    def test_get_error_by_false_email(self, test_client: TestClient):
        response = test_client.get("/api/user_by_email/wrong@false.com")
        assert response.status_code == 404

# GET /api/user_by_name/{name}
class TestGetUserByUserName:
    # get user by name
    def test_get_existing_user_by_name(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        response = test_client.get(f"/api/user_by_name/{CARL["name"]}")
        assert response.status_code == 200
        temp = response.json()
        assert temp["userId"] is not None
        assert temp["name"] == CARL["name"]
        assert temp["email"] == CARL["email"]
        assert "password" not in temp
        assert "pass_hash" not in temp
        assert temp["createdAt"] is not None

    # error name does not exist
    def test_get_error_by_false_user_name(self, test_client: TestClient):
        response = test_client.get("/api/user_by_name/false-name")
        assert response.status_code == 404

# POST /api/user
class TestPostUser:
    # create new user
    def test_create_new_user(self, test_client: TestClient):
        response = test_client.post("/api/signup", json=CARL)
        assert response.status_code == 201
    
    # error existing user
    def test_error_existing_user(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        response = test_client.post("/api/signup", json=CARL)
        assert response.status_code == 409
    
    # error wrong syntax
    def test_error_incomplete_user(self, test_client: TestClient):
        response = test_client.post("/api/signup", json={"name": "Carl"})
        assert response.status_code == 422

# PUT /api/user
class TestPutUser:
    # update user
    def test_update_existing_user(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        user_id = test_client.get("/api/users").json()[0]["userId"]
        response = test_client.put("/api/user", json={
            "userId": user_id,
            "name": CARL_UPDATED["name"],
            "email": CARL_UPDATED["email"],
            "password": CARL_UPDATED["password"]
        })
        assert response.status_code == 204
    
    # error not existing user
    def test_error_user_id_does_not_exist(self, test_client: TestClient):
        response = test_client.put("/api/user", json={
            "userId": "false-user-id",
            "name": CARL_UPDATED["name"],
            "email": CARL_UPDATED["email"],
            "password": CARL_UPDATED["password"]
        })
        assert response.status_code == 404
    
    # update only one field
    def test_error_incomplete_request_body(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        user_id = test_client.get("/api/users").json()[0]["userId"]
        response = test_client.put("/api/user", json={
            "userId": user_id,
            "email": CARL_UPDATED["email"]
        })
        assert response.status_code == 204
        response2 = test_client.get(f"/api/user_by_name/{CARL["name"]}")
        assert response2.status_code == 200
        res_json = response2.json()
        assert res_json["name"] == CARL["name"]
        assert res_json["email"] == CARL_UPDATED["email"]

# DELETE /api/user
class TestDeleteUser:
    # delete user
    def test_delete_existing_user(self, test_client: TestClient):
        test_client.post("/api/signup", json=CARL)
        user_id = test_client.get("/api/users").json()[0]["userId"]
        response = test_client.delete(f"/api/user/{user_id}")
        assert response.status_code == 200
    
    # error not existing user
    def test_error_user_does_not_exist(self, test_client: TestClient):
        response = test_client.delete(f"/api/user/false-user-id")
        assert response.status_code == 404
