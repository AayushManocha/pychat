from fastapi.testclient import TestClient
from app.server import app
from app.database.db import CHATS


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
  assert len(response_json) == 1

def test_authenticated_user_create_message():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 201

  response_json = response.json()
  assert response_json["message"] == "hello"

def test_when_a_user_sends_initial_message_to_another_user_a_chat_should_be_created():
  initial_chat_length = len(CHATS)

  response = test_client.post("/message", json={"to_id": "3", "message": "hello Luke"})
  assert response.status_code == 201
  assert len(CHATS) == initial_chat_length + 1

  found_chat = None
  for chat in CHATS:
    if chat["user1_id"] == "1" and chat["user2_id"] == "3":
      found_chat = chat
      break

  assert found_chat

def test_when_a_user_sends_a_message_to_another_user_the_chat_should_not_be_created_if_it_already_exists():
  response = test_client.post("/message", json={"to_id": "2", "message": "hello mark"})

  initial_chat_length = len(CHATS)
  assert response.status_code == 201
  assert len(CHATS) == initial_chat_length

def test_a_user_can_view_their_chats():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/chat")
  assert response.status_code == 200

  response_json = response.json()
  assert "user1_name" in response_json[0]
  assert "user2_name" in response_json[0]


def test_unautenticated_create_message():
  test_client.cookies["_pychat"] = "" # clear the cookie
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 401




