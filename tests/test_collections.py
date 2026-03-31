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

def populate_database(test_client: TestClient, amount: int):
    user_id = create_user_and_get_user_id(test_client=test_client)
    for i in range(amount):
        test_client.post("/api/collection", json={
            "userId": user_id,
            "title": f"Title {i + 1}"
        })
    return user_id

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

class TestGetPopularCollections:
    # popular collections
    def test_get_popular_collections(self, test_client: TestClient):
        populate_database(test_client=test_client, amount=10)
        response = test_client.get("/api/collections/popular")
        assert len(response.json()) == 5
        assert response.status_code == 200

class TestGetCollectionById:
    # collection by id
    def test_get_collection_by_id(self, test_client: TestClient):
        user_id = populate_database(test_client=test_client, amount=1)
        collection_id = test_client.get(f"/api/user/{user_id}").json()["collections"][0]["collectionId"]
        response = test_client.get(f"/api/collection/{collection_id}")
        res_json = response.json()
        assert res_json["user"]["userId"] == user_id
        assert res_json["collectionId"] == collection_id
        assert res_json["title"] == "Title 1"
        assert response.status_code == 200
    
    # error id does not exist
    def test_error_collection_id_does_not_exist(self, test_client: TestClient):
        populate_database(test_client=test_client, amount=1)
        response = test_client.get("/api/collection/wrong-collection-id")
        assert response.status_code == 404

class TestPostCollection:
    # post collection
    def test_post_collection(self, test_client: TestClient):
        user_id = create_user_and_get_user_id(test_client=test_client)
        response = test_client.post("/api/collection", json={
            "userId": user_id,
            "title": "Test Title"
        })
        assert response.status_code == 201
    
    # error user does not exist
    def test_error_user_does_not_exist(self, test_client: TestClient):
        create_user_and_get_user_id(test_client=test_client)
        response = test_client.post("/api/collection", json={
            "userId": "wrong-user-id",
            "title": "Test Title"
        })
        assert response.status_code == 404
    
    # error wrong body format
    def test_error_post_wrong_body_format(self, test_client: TestClient):
        create_user_and_get_user_id(test_client=test_client)
        response = test_client.post("/api/collection", json={
            "userId": "wrong-user-id",
            "description": "Title missing"
        })
        assert response.status_code == 422

class TestPutCollection:
    # put collection
    def test_put_collection(self, test_client: TestClient):
        user_id = populate_database(test_client=test_client, amount=1)
        collection_id = test_client.get(f"/api/user/{user_id}").json()["collections"][0]["collectionId"]
        response1 = test_client.put("/api/collection", json={
            "collectionId": collection_id,
            "title": "Updated Title"
        })
        assert response1.status_code == 204
        response2 = test_client.get(f"/api/collection/{collection_id}")
        assert response2.json()["title"] == "Updated Title"
    
    # error collection id does not exist
    def test_error_collection_id_does_not_exist(self, test_client: TestClient):
        populate_database(test_client=test_client, amount=1)
        response = test_client.put("/api/collection", json={
            "collectionId": "wrong-collection-id",
            "title": "Updated Title"
        })
        assert response.status_code == 404
    
    # error wrong body format
    def test_error_put_wrong_body_format(self, test_client: TestClient):
        populate_database(test_client=test_client, amount=1)
        response = test_client.put("/api/collection", json={
            "title": "collection id missing",
            "description": "collection id missing"
        })
        assert response.status_code == 422

class TestDeleteCollection:
    # delete collection
    def test_delete_collection(self, test_client: TestClient):
        user_id = populate_database(test_client=test_client, amount=1)
        collection_id = test_client.get(f"/api/user/{user_id}").json()["collections"][0]["collectionId"]
        response1 = test_client.delete(f"/api/collection/{collection_id}")
        response2 = test_client.get(f"/api/collection/{collection_id}")
        assert response1.status_code == 204
        assert response2.status_code == 404
    
    # error collection id does not exist
    def test_error_delete_collection_id_does_not_exist(self, test_client: TestClient):
        user_id = populate_database(test_client=test_client, amount=1)
        collection_id = test_client.get(f"/api/user/{user_id}").json()["collections"][0]["collectionId"]
        response1 = test_client.delete("/api/collection/wrong-collection-id")
        response2 = test_client.get(f"/api/collection/{collection_id}")
        assert response1.status_code == 404
        assert response2.status_code == 200
