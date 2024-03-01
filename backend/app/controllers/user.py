from fastapi import APIRouter
from sqlalchemy import text

from app.database.db import User, get_new_db_session


user_router = APIRouter()

@user_router.get("/user/search/{searchTerm}")
async def get_user(searchTerm: str):
  with get_new_db_session() as db:
    users = db.query(User).where(User.username.like(f"%{searchTerm}%")).all()
  return users

