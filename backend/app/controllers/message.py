
from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.database.db import MESSAGES
from .utils.authentication_middleware import get_current_user


message_router = APIRouter()

class CreateMessageRequest(BaseModel):
    to_id: str
    message: str

@message_router.post("/message", status_code=201)
async def create_message(request: Request, create_message_request: CreateMessageRequest, status_code=201):
  user = get_current_user(request)
  new_message = {
    'id': str(len(MESSAGES) + 1),
    'from_id': user['id'],
    'to_id': create_message_request.to_id,
    'message': create_message_request.message
  }

  MESSAGES.append(new_message)
  return new_message

@message_router.get("/message")
async def get_messages(request: Request):
  user = get_current_user(request)
  MESSAGES_TO_USER = [m for m in MESSAGES if m['to_id'] == user['id']]
  print(F'MESSAGES_TO_USER: {MESSAGES_TO_USER}')
  return MESSAGES_TO_USER