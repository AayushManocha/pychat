from fastapi.testclient import TestClient
from app.server import app


test_client = TestClient(app)

def test_login():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  assert response.status_code == 200
  assert response.cookies["_pychat"]

def test_get_messages():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/message")
  assert response.status_code == 200

  response_json = response.json()
  assert len(response_json) == 0

def test_authenticated_user_create_message():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 201

  response_json = response.json()
  assert response_json["from_id"] == "1"
  assert response_json["to_id"] == "1"
  assert response_json["message"] == "hello"

def test_unautenticated_create_message():
  test_client.cookies["_pychat"] = "" # clear the cookie
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 401



