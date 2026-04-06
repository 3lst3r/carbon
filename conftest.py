import pytest
import mongomock
from unittest.mock import patch
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def mock_collections():
    mongo_client = mongomock.MongoClient()
    db = mongo_client["carbon_db"]
    return {
        "db": db,
        "users": db["users"],
        "collections": db["collections"],
        "cards": db["cards"],
        "favorites": db["favorites"],
        "categories": db["categories"]
    }

@pytest.fixture(scope="function")
def client(mock_collections: dict):
    with (
        patch("src.database.db", mock_collections["db"]),
        patch("src.database.users_table", mock_collections["users"]),
        patch("src.database.collections_table", mock_collections["collections"]),
        patch("src.database.cards_table", mock_collections["cards"]),
        patch("src.database.favorites_table", mock_collections["favorites"]),
        patch("src.database.categories_table", mock_collections["categories"]),
    ):
        from src.main import app
        from src.database import initialize_categories
        initialize_categories()
        yield TestClient(app), mock_collections

@pytest.fixture(scope="function")
def test_client(client) -> TestClient:
    http_client, _ = client
    return http_client
