from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.database.db import CHATS, MESSAGES, USERS
from .utils.authentication_middleware import get_current_user


message_router = APIRouter()

class CreateMessageRequest(BaseModel):
    to_id: str
    message: str

@message_router.post("/message", status_code=201)
async def create_message(request: Request, create_message_request: CreateMessageRequest, status_code=201):
  user = get_current_user(request)

  user_exists = False
  for u in USERS:
    if u['id'] == create_message_request.to_id:
      user_exists = True
      break
  
  if not user_exists:
    raise HTTPException(status_code=404, detail="User not found")
  
  existing_chat = None
  for chat in CHATS:
    if chat['user1_id'] == user['id'] and chat['user2_id'] == create_message_request.to_id or chat['user1_id'] == create_message_request.to_id and chat['user2_id'] == user['id']:
      existing_chat = chat
      break

  if not existing_chat:
    new_chat = {
      'id': str(len(CHATS) + 1),
      'user1_id': user['id'],
      'user2_id': create_message_request.to_id
    }
    CHATS.append(new_chat)


  new_message = {
    'id': str(len(MESSAGES) + 1),
    'chat_id': existing_chat['id'] if existing_chat else new_chat['id'],
    'message': create_message_request.message
  }

  MESSAGES.append(new_message)
  return new_message

@message_router.get("/chat/{chat_id}/message")
async def get_messages(request: Request, chat_id: int):
  user = get_current_user(request)

  chat = None
  for c in CHATS:
    if c['id'] == str(chat_id):
      chat = c
      break

  user_in_chat = chat['user1_id'] == user['id'] or chat['user2_id'] == user['id']

  if not user_in_chat:
    raise HTTPException(status_code=404, detail="Chat not found")

  messages_in_chat = [m for m in MESSAGES if m['chat_id'] == str(chat_id)]

  return messages_in_chat
