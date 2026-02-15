
# GET all users (locked)
GET_ALL_USERS = {
    "totalUsers": 3,
    "users": [
        {
            "userId": "example-uuid-user-1",
            "name": "Alice"
        },
        {
            "userId": "example-uuid-user-2",
            "name": "Bob"
        },
        {
            "userId": "example-uuid-user-3",
            "name": "Carl"
        }
    ]
}

# GET user by name
# GET user by user_id
GET_USER = {
    "userId": "example-uuid-user-1",
    "name": "Alice",
    "totalCollections": 3,
    "collections": [
        {
            "user_id": "example-uuid-user-1",
            "collection_id": "example-uuid-collection-1",
            "title": "Title 1",
            "description": "Description 1",
            "color": "red"
        },
        {
            "user_id": "example-uuid-user-1",
            "collection_id": "example-uuid-collection-2",
            "title": "Title 2",
            "description": "Description 2",
            "color": "green"
        },
        {
            "user_id": "example-uuid-user-1",
            "collection_id": "example-uuid-collection-3",
            "title": "Title 3",
            "description": "Description 3",
            "color": "blue"
        }
    ]
}


# POST user
POST_USER = {
    "userId": "example-uuid-user-4",
    "name": "Diana"
}

# PUT user
PUT_USER = {
    "userId": "example-uuid-user-1",
    "name": "Anna"
}

# DELETE user
DELETE_USER = 204

# GET all collections (locked)
GET_ALL_COLLECTIONS = {
    "totalCollections": 4,
    "collections": [
        {
            "userId": "example-uuid-user-1",
            "collectionId": "example-uuid-collection-1",
            "title": "Title 1",
            "description": "Description 1",
            "color": "red"
        },
        {
            "userId": "example-uuid-user-1",
            "collectionId": "example-uuid-collection-2",
            "title": "Title 2",
            "description": "Description 2",
            "color": "green"
        },
        {
            "userId": "example-uuid-user-1",
            "collectionId": "example-uuid-collection-3",
            "title": "Title 3",
            "description": "Description 3",
            "color": "blue"
        },
        {
            "userId": "example-uuid-user-2",
            "collectionId": "example-uuid-collection-4",
            "title": "Title 4",
            "description": "Description 4",
            "color": "yellow"
        }
    ]
}

# GET collection by collection_id
# PUT collection by collection_id
GET_PUT_COLLECTION = {
    "userId": "example-uuid-user-1",
    "collectionId": "example-uuid-collection-1",
    "title": "Title 1",
    "description": "Description 1",
    "color": "red",
    "totalCards": 5,
    "cards": [
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-1",
            "front": "Front 1",
            "back": "Back 1"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-2",
            "front": "Front 2",
            "back": "Back 2"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-3",
            "front": "Front 3",
            "back": "Back 3"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-4",
            "front": "Front 4",
            "back": "Back 4"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-5",
            "front": "Front 5",
            "back": "Back 5"
        }
    ]
}

# POST collection by user_id
POST_COLLECTION = {
    "userId": "example-uuid-user-1",
    "collectionId": "example-uuid-collection-67",
    "title": "Empty Collection 1",
    "description": "Empty Description 1",
    "color": "green",
    "totalCards": 0,
    "cards": []
}

# DELETE collection by collection_id
DELETE_COLLECTION = 204

# GET all cards (locked)
GET_ALL_CARDS = {
    "totalCards": 6,
    "cards": [
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-1",
            "front": "Front 1",
            "back": "Back 1"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-2",
            "front": "Front 2",
            "back": "Back 2"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-3",
            "front": "Front 3",
            "back": "Back 3"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-4",
            "front": "Front 4",
            "back": "Back 4"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-5",
            "front": "Front 5",
            "back": "Back 5"
        },
        {
            "collectionId": "example-uuid-collection-2",
            "cardId": "example-uuid-card-6",
            "front": "Front 6",
            "back": "Back 6"
        }
    ]
}

# GET card by card_id
# PUT card by card_id
GET_PUT_CARD = {
    "collectionId": "example-uuid-collection-2",
    "cardId": "example-uuid-card-6",
    "front": "Front 6",
    "back": "Back 6"
}

# POST cards by collection_id
POST_CARDS = {
    "cards": [
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-1",
            "front": "Front 1",
            "back": "Back 1"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-2",
            "front": "Front 2",
            "back": "Back 2"
        },
        {
            "collectionId": "example-uuid-collection-1",
            "cardId": "example-uuid-card-3",
            "front": "Front 3",
            "back": "Back 3"
        }
    ]
}

# DELETE card by card_id
DELETE_CARD = 204

# GET all categories
GET_ALL_CATEGORIES = {
    "categories": [
        {
            "categoryName": "Category 1",
            "subCategories": [
                {
                    "subCategoryName": "Sub Category 1"
                },
                {
                    "subCategoryName": "Sub Category 2"
                },
                {
                    "subCategoryName": "Sub Category 3"
                }
            ]
        },
        {
            "categoryName": "Category 2",
            "subCategories": [
                {
                    "subCategoryName": "Sub Category 4"
                },
                {
                    "subCategoryName": "Sub Category 5"
                },
                {
                    "subCategoryName": "Sub Category 6"
                }
            ]
        },
        {
            "categoryName": "Category 3",
            "subCategories": [
                {
                    "subCategoryName": "Sub Category 7"
                },
                {
                    "subCategoryName": "Sub Category 8"
                },
                {
                    "subCategoryName": "Sub Category 9"
                }
            ]
        },
    ]
}

# POST signup
# POST login
POST_SIGNUP_LOGIN = {
    "token": "example-jwt-cookie-token"
}

# DELETE login
DELETE_LOGIN = 204

# GET health
HEALTH = {
    "status": "ok", 
    "database": "up"
}

# POST save collection
POST_SAVE_COLLECTION = {
    "userId": "example-uuid-user-3-of-user-that-saved-this-collection",
    "collectionId": "example-uuid-collection-2"
}

# GET all saved collections
GET_SAVED_COLLECTIONS = {
    "totalCollections": 2,
    "collections": [
        {
            "userId": "example-uuid-user-1",
            "collectionId": "example-uuid-collection-1",
            "title": "Title 1",
            "description": "Description 1",
            "color": "red"
        },
        {
            "userId": "example-uuid-user-2",
            "collectionId": "example-uuid-collection-4",
            "title": "Title 4",
            "description": "Description 4",
            "color": "yellow"
        }
    ]
}