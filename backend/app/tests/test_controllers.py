from fastapi.testclient import TestClient
import pytest
from app.server import app
from app.database.db import CHATS
from app.database import db


test_client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_tests():
  db.clear_db()
  db.seed_db()


def test_login():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  assert response.status_code == 200
  assert response.cookies["_pychat"]

def test_can_search_for_users_by_username():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/user/search/jo")
  assert response.status_code == 200

  response_json = response.json()
  assert len(response_json) == 1
  assert response_json[0]["username"] == "john"

def test_can_get_messages_by_chat_id():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/chat/1/message")
  assert response.status_code == 200

  response_json = response.json()

def messages_include_sender_name():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/chat/1/message")
  assert response.status_code == 200

  response_json = response.json()
  assert "sender_id" in response_json[0]

def test_authenticated_user_create_message():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 201

  response_json = response.json()
  print(f'response_json: {response_json}')
  assert response_json["message"] == "hello"

def test_when_a_user_sends_initial_message_to_another_user_a_chat_should_be_created():

  response = test_client.post("/message", json={"to_id": "3", "message": "hello Luke"})
  assert response.status_code == 201

  with db.get_new_db_session() as s:
    chat = s.query(db.Chat).filter(db.Chat.user1_id == 1, db.Chat.user2_id == 3).first()
    assert chat is not None


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
  print(f'response_json: {response_json}')
  assert "user1_name" in response_json[0]
  assert "user2_name" in response_json[0]

def test_a_user_can_get_chat_data_if_they_are_member_of_chat():
  response = test_client.post("/login", json={"username": "john", "password": "password"})
  response = test_client.get("/chat/1")
  assert response.status_code == 200

  response_json = response.json()
  assert response_json["user1_id"] == 1
  assert response_json["user2_id"] == 2


def test_unauthenticated_cannot_create_message():
  test_client.cookies["_pychat"] = "" # clear the cookie
  response = test_client.post("/message", json={"to_id": "1", "message": "hello"})
  assert response.status_code == 401




