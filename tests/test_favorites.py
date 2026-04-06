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

def create_collection_and_get_collection_id(test_client: TestClient):
    test_client.post("/api/signup", json=CARL)
    user_id = test_client.get("/api/user_by_name/Carl").json()["userId"]
    test_client.post("/api/collection", json={
        "userId": user_id,
        "title": "Test Title"
    })
    collection_id = test_client.get(f"/api/user/{user_id}").json()["collections"][0]["collectionId"]
    return user_id, collection_id

class TestPostFavorite:
    # post favorite
    def test_post_favorite(self, test_client: TestClient):
        user_id, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": collection_id
        })
        assert response.status_code == 201
    
    # error user id does not exist
    def test_error_post_user_id_does_not_exist(self, test_client: TestClient):
        _, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.post("/api/save", json={
            "userId": "wrong-user-id",
            "collectionId": collection_id
        })
        assert response.status_code == 404

    # error collection id does not exist
    def test_error_post_collection_id_does_not_exist(self, test_client: TestClient):
        user_id, _ = create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": "wrong-collection-id"
        })
        assert response.status_code == 404

    # error both ids do not exist
    def test_error_post_both_ids_do_not_exist(self, test_client: TestClient):
        create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.post("/api/save", json={
            "userId": "wrong-user-id",
            "collectionId": "wrong-collection-id"
        })
        assert response.status_code == 404

class TestGetAllFavorites:
    # get all favorites
    def test_get_all_favorites_empty(self, test_client: TestClient):
        response = test_client.get("/api/saved")
        assert response.status_code == 200
        assert type(response.json()) == type([])
        assert len(response.json()) == 0
    
    # get all favorites filled
    def test_get_all_favorites_filled(self, test_client: TestClient):
        user_id, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": collection_id
        })
        response = test_client.get("/api/saved")
        assert response.status_code == 200
        assert type(response.json()) == type([])
        assert len(response.json()) == 1

class TestGetFavorite:
    # get favorites from user
    def test_get_favorite(self, test_client: TestClient):
        user_id, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": collection_id
        })
        response = test_client.get(f"/api/saved/{user_id}")
        assert response.status_code == 200
        assert type(response.json()) == type([])
        assert len(response.json()) == 1
    
    # get favorites from user empty
    def test_error_get_favorite_does_not_exist(self, test_client: TestClient):
        user_id, _ = create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.get(f"/api/saved/{user_id}")
        assert response.status_code == 200
        assert type(response.json()) == type([])
        assert len(response.json()) == 0

    # error user does not exist
    def test_error_get_favorite_user_does_not_exist(self, test_client: TestClient):
        create_collection_and_get_collection_id(test_client=test_client)
        response = test_client.get("/api/saved/wrong-user-id")
        assert response.status_code == 404

class TestDeleteFavorite:
    # delete favorite
    def test_delete_favorite(self, test_client: TestClient):
        user_id, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": collection_id
        })
        response = test_client.request(
            method="DELETE",
            url="/api/saved",
            json={
                "userId": user_id,
                "collectionId": collection_id
            }
        )
        assert response.status_code == 204

    # error favorite does not exist
    def test_error_delete_favorite_does_not_exist(self, test_client: TestClient):
        user_id, collection_id = create_collection_and_get_collection_id(test_client=test_client)
        test_client.post("/api/save", json={
            "userId": user_id,
            "collectionId": collection_id
        })
        response = test_client.request(
            method="DELETE",
            url="/api/saved",
            json={
                "userId": user_id,
                "collectionId": "wrong-collection-id"
            }
        )
        assert response.status_code == 404