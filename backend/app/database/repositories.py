from typing import List
from app.database.db import Chat, User, get_new_db_session, Message
from app.database import db
from sqlalchemy import text

class UserRepository:
   def get_user_by_id(self, user_id: str) -> User:
      with get_new_db_session() as s:
          result = s.query(User).filter(User.id == user_id).first()
      return result


class ChatRepository:

    def get_chat_by_id(self, chat_id: int) -> Chat:
      results = None
      with get_new_db_session() as s:
          result = s.query(Chat).filter(Chat.id == chat_id).first()
      return result
    
    def get_chat_by_user_ids(self, user1_id: str, user2_id: str) -> Chat:
      with get_new_db_session() as s:
          result = s.query(Chat).filter(Chat.user1_id == user1_id, Chat.user2_id == user2_id).first()
          if not result:
            result = s.query(Chat).filter(Chat.user1_id == user2_id, Chat.user2_id == user1_id).first()
      return result

    def get_chats_by_user_id(self, user_id: str):
      with get_new_db_session() as s:
          results = s.query(Chat).filter(text(f"user1_id = '{user_id}' or user2_id = '{user_id}'")).all()
      return results

    def create_chat(self, user1_id: str, user2_id: str) -> Chat:
      with get_new_db_session() as s:
          chat = Chat(user1_id=user1_id, user2_id=user2_id)
          s.add(chat)
          s.commit()
      return chat
    
class MessageRepository:
  def create_message(self, chat_id: int, message: str) -> Message:
    with get_new_db_session() as s:
        chat = s.query(Chat).filter(Chat.id == chat_id).first()
        # message = Message(message=message, chat=chat)
        message = Message(message=message)
        s.add(message)
        s.commit()
    return message
