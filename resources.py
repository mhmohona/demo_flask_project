# resources.py

# API tokens mapped to user IDs
Tokens = {
    "user1Token": "user1",
    "user2Token": "user2",
    "adminToken": "admin",
}

# User roles
Users = {
    "user1": {
        "role": "user",
        "department": "engineering",
    },
    "user2": {
        "role": "user",
        "department": "marketing",
    },
    "admin": {
        "role": "admin",
        "department": "management",
    },
}

# TODO items
TodoItems = {
    "1": {
        "id": "1",
        "user": "user1",
        "title": "Learn Flask",
        "status": "pending",
        "public": "false"
    },
    "2": {
        "id": "2",
        "user": "user2",
        "title": "Learn Cerbos",
        "status": "completed",
        "public": "false"
    },
    "3": {
        "id": "3",
        "user": "user1",
        "title": "Develop REST API",
        "status": "in_progress",
        "public": "true"
    }
}