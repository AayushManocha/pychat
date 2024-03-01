from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.database.db import Chat, get_new_db_session, Message
from .utils.authentication_middleware import get_current_user


message_router = APIRouter()

class CreateMessageRequest(BaseModel):
    to_id: str
    message: str

@message_router.post("/message", status_code=201)
async def create_message(request: Request, create_message_request: CreateMessageRequest, status_code=201):
  user = get_current_user(request)

  with get_new_db_session() as s:
    chat1 = s.query(Chat).filter(Chat.user1_id == user['id'], Chat.user2_id == create_message_request.to_id).first()
    chat2 = s.query(Chat).filter(Chat.user1_id == create_message_request.to_id, Chat.user2_id == user['id']).first()

    chat = chat1 or chat2

    if not chat:
      chat = Chat(user1_id=user['id'], user2_id=create_message_request.to_id)
      s.add(chat)
      s.commit()

    new_message = Message(message=create_message_request.message)
    chat.messages.append(new_message)
    s.commit()
    new_message = new_message.to_dict()

  return new_message    


@message_router.get("/chat/{chat_id}/message")
async def get_messages(request: Request, chat_id: int):
  user = get_current_user(request)

  chat = None
  with get_new_db_session() as s:
    chat = s.query(Chat).filter(Chat.id == chat_id).first()

  if not chat:
    raise HTTPException(status_code=404, detail="Chat not found")

  user_in_chat = chat.user1_id == user['id'] or chat.user2_id == user['id']

  if not user_in_chat:
    raise HTTPException(status_code=403, detail="User is not a member of this chat")

  messages = None
  with get_new_db_session() as s:
    chat = s.query(Chat).filter(Chat.id == chat_id).first()
    messages = chat.messages
  return messages

