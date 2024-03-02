USERS = [
  {'id':'1', "username": "john", "password": "password"},
  {'id':'2', "username": "mark", "password": "password"},
  {'id':'3', "username": "luke", "password": "password"}
]

MESSAGES = [
  {'id':'1', "chat_id": "1", "message": "Hello Mark", "sender_id": "1"},
  {'id':'2', "chat_id": "1", "message": "Hello John", "sender_id": "2"},

  # {'id':'3', "chat_id": "2", "message": "Hello Luke"},
  # {'id':'4', "chat_id": "2", "message": "Hello John"},
  # {'id':'5', "chat_id": "2", "message": "What're mans saying"},

]

CHATS = [
  {'id':'1', "user1_id": "1", "user2_id": "2"},

  # {'id':'2', "user1_id": "1", "user2_id": "3"},
]


import datetime
from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List

class ToDictMixin:
  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}  


ENGINE = create_engine('sqlite:///./app.db')

class Base(DeclarativeBase, ToDictMixin):
  __abstract__ = True
  # created_at = mapped_column(DateTime, default=datetime.datetime.now)
  # updated_at = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class User(Base):
  __tablename__ = 'users'
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  username: Mapped[str] = mapped_column(String, unique=True, index=True)
  password: Mapped[str] = mapped_column(String)

  chats_as_user1: Mapped[List['Chat']] = relationship("Chat", foreign_keys="Chat.user1_id", back_populates="user1")
  chats_as_user2: Mapped[List['Chat']] = relationship("Chat", foreign_keys="Chat.user2_id", back_populates="user2")

class Message(Base):
  __tablename__ = 'messages'
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  message: Mapped[str] = mapped_column(String)

  chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)
  chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

  sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
  sender: Mapped["User"] = relationship("User")

class Chat(Base):
  __tablename__ = 'chats'
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

  user1_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
  user1: Mapped["User"] = relationship("User", foreign_keys=[user1_id])

  user2_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
  user2: Mapped["User"] = relationship("User", foreign_keys=[user2_id])

  messages: Mapped[List['Message']] = relationship("Message", back_populates="chat")

def seed_db():
  session = Session(ENGINE)
  for user in USERS:
    new_user = User(**user)
    session.add(new_user)

  for chat in CHATS:
    new_chat = Chat(**chat)
    session.add(new_chat)

  for message in MESSAGES:
    new_message = Message(**message)
    session.add(new_message)

  session.commit()

def clear_db():
  try:
    session = Session(ENGINE)
    session.query(User).delete()
    session.query(Chat).delete()
    session.query(Message).delete()
    session.commit()
  except:
    pass

def create_db():
  Base.metadata.create_all(ENGINE)

def get_new_db_session() -> Session:
  return Session(ENGINE)