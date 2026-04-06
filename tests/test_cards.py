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
    return collection_id

class TestGetAllCards:
    # empty card list
    def test_empty_card_list(self, test_client: TestClient):
        response = test_client.get("/api/cards")
        assert response.status_code == 200
        assert response.json() == []
    
    # filled card list
    def test_filled_card_list(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        test_client.post("/api/card", json={
            "collectionId": collection_id,
            "cards": [
                {
                    "front": "front 1",
                    "back": "back 1",
                    "notes": "notes 1"
                }
            ]
        })
        response = test_client.get("/api/cards")
        assert response.status_code == 200
        assert response.json()[0]["front"] == "front 1"

class TestGetCardById:
    # card by id
    def test_get_card_by_id(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        front = "test front"
        back = "test back"
        notes = "test notes"
        test_client.post("/api/card", json={
            "collectionId": collection_id,
            "cards": [
                {
                    "front": front,
                    "back": back,
                    "notes": notes
                }
            ]
        })
        res = test_client.get("/api/cards")
        card_id = res.json()[0]["cardId"]
        response = test_client.get(f"/api/card/{card_id}")
        assert response.status_code == 200
        assert response.json()["cardId"] == card_id
        assert response.json()["front"] == front
        assert response.json()["back"] == back
        assert response.json()["notes"] == notes
    
    # error card id does not exist
    def test_error_get_card_id_does_not_exist(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        front = "test front"
        back = "test back"
        notes = "test notes"
        test_client.post("/api/card", json={
            "collectionId": collection_id,
            "cards": [
                {
                    "front": front,
                    "back": back,
                    "notes": notes
                }
            ]
        })
        response = test_client.get("/api/card/wrong-card-id")
        assert response.status_code == 404

class TestPostCard:
    # post card by id
    def test_post_card_by_id(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        front = "test front"
        back = "test back"
        notes = "test notes"
        response = test_client.post("/api/card", json={
            "collectionId": collection_id,
            "cards": [
                {
                    "front": front,
                    "back": back,
                    "notes": notes
                }
            ]
        })
        assert response.status_code == 201
    
    # error collection id does not exist
    def test_error_collection_id_does_not_exist(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        front = "test front"
        back = "test back"
        notes = "test notes"
        response = test_client.post("/api/card", json={
            "collectionId": "wrong-collection-id",
            "cards": [
                {
                    "front": front,
                    "back": back,
                    "notes": notes
                }
            ]
        })
        assert response.status_code == 404
    
    # error wrong body format
    def test_error_post_wrong_body_format(self, test_client: TestClient):
        collection_id = create_collection_and_get_collection_id(test_client=test_client)
        front = "test front"
        back = "test back"
        notes = "test notes"
        response = test_client.post("/api/card", json={
            "collectionId": collection_id,
            "cards": [
                {
                    "wrongFrontField": front,
                    "back": back,
                    "notes": notes
                }
            ]
        })
        assert response.status_code == 422

class TestPutCard:
    # put card by card id
    def test_put_card_by_id(self, test_client: TestClient):
        assert True
    
    # error card id does not exist
    def test_error_put_card_id_does_not_exist(self, test_client: TestClient):
        assert True
    
    # error wrong body format
    def test_error_put_wrong_body_format(self, test_client: TestClient):
        assert True

class TestDeleteCard:
    # delete card by id
    def test_delete_card_by_id(self, test_client: TestClient):
        assert True
    
    # error card id does not exist
    def test_error_delete_card_id_does_not_exist(self, test_client: TestClient):
        assert True