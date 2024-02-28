from fastapi import APIRouter, Request

from app.controllers.utils.authentication_middleware import get_current_user
from app.database.db import CHATS
from app.database.db import USERS


chat_router = APIRouter()

@chat_router.get("/chat")
def chat_index(request: Request):
  user = get_current_user(request)
  user_chats = [chat for chat in CHATS if chat['user1_id'] == user['id'] or chat['user2_id'] == user['id']]

  # Add the user's name to the chat
  for chat in user_chats:
    if chat['user1_id'] == user['id']:
      chat['user2_name'] = next(user['username'] for user in USERS if user['id'] == chat['user2_id'])
    else:
      chat['user1_name'] = next(user['username'] for user in USERS if user['id'] == chat['user1_id'])

  return user_chats