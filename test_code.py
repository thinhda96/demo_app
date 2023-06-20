import pytest
from fastapi.testclient import TestClient
from code import app, User, users

client = TestClient(app)

def test_create_user():
    user = User(id=1, name="John Doe", email="john.doe@example.com", password="password123")
    response = client.post("/users", json=user.dict())
    assert response.status_code == 200
    assert response.json() == {"success": True, "data": user.dict()}

def test_create_existing_user():
    user = User(id=1, name="John Doe", email="john.doe@example.com", password="password123")
    response = client.post("/users", json=user.dict())
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_read_user():
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"success": True, "data": users[user_id].dict()}

def test_read_nonexistent_user():
    user_id = 999
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user():
    user_id = 1
    updated_user = User(id=1, name="Jane Doe", email="jane.doe@example.com", password="password456")
    response = client.put(f"/users/{user_id}", json=updated_user.dict())
    assert response.status_code == 200
    assert response.json() == {"success": True, "data": updated_user.dict()}

def test_update_nonexistent_user():
    user_id = 999
    updated_user = User(id=999, name="Jane Doe", email="jane.doe@example.com", password="password456")
    response = client.put(f"/users/{user_id}", json=updated_user.dict())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_delete_user():
    user_id = 1
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"success": True, "data": None}

def test_delete_nonexistent_user():
    user_id = 999
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}