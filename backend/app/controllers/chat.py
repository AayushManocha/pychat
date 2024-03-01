from fastapi import APIRouter, HTTPException, Request

from app.controllers.utils.authentication_middleware import get_current_user
from app.database.db import CHATS, Chat, get_new_db_session
from app.database.db import USERS
from app.database.repositories import ChatRepository, UserRepository


chat_router = APIRouter()

@chat_router.get("/chat")
async def chat_index(request: Request):
  user = get_current_user(request)

  chats = ChatRepository().get_chats_by_user_id(user['id'])
  chats = [chat.to_dict() for chat in chats]

  for chat in chats:
    chat['user1_name'] = UserRepository().get_user_by_id(chat['user1_id']).username
    chat['user2_name'] = UserRepository().get_user_by_id(chat['user2_id']).username

  return chats

@chat_router.get("/chat/{chat_id}")
async def chat_index(request: Request, chat_id: int):
  user = get_current_user(request)

  with get_new_db_session() as s:
    chat = s.query(Chat).filter(Chat.id == chat_id).first()

  user_in_chat = chat.user1_id == user['id'] or chat.user2_id == user['id']

  if not user_in_chat:
    raise HTTPException(status_code=401, detail="Unauthorized")
  


  # chat['user1_name'] = USERS[int(chat['user1_id']) - 1]['username']
  # chat['user2_name'] = USERS[int(chat['user2_id']) - 1]['username']

  return chat