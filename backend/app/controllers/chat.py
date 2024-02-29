from fastapi import APIRouter, Request

from app.controllers.utils.authentication_middleware import get_current_user
from app.database.db import CHATS
from app.database.db import USERS


chat_router = APIRouter()

@chat_router.get("/chat")
def chat_index(request: Request):
  user = get_current_user(request)
  chats_for_current_user = []
  for chat in CHATS:
    if chat['user1_id'] == user['id'] or chat['user2_id'] == user['id']:
      chats_for_current_user.append(chat)

  # Add the user's name to the chat
  for chat in chats_for_current_user:
    chat['user1_name'] = USERS[int(chat['user1_id']) - 1]['username']
    chat['user2_name'] = USERS[int(chat['user2_id']) - 1]['username']

  return chats_for_current_user 