from fastapi import APIRouter, HTTPException, Request, Response
import jwt
from pydantic import BaseModel
from app.database.db import USERS, User, get_new_db_session
from app.controllers.utils.authentication_middleware import get_current_user


auth_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login")
async def login(login_request: LoginRequest, response: Response, status_code=200):
  username = login_request.username
  password = login_request.password

  password_is_valid = False
  with get_new_db_session() as s:
    user = s.query(User).filter(User.username == username).first()
    print(f'user: {user}')
    if user:
      password_is_valid = user.password == password

  if password_is_valid:

    token = jwt.encode(user.to_dict(), 'secret', algorithm='HS256')
    response.set_cookie(key="_pychat", value=token)
    return {"message": "Login successful", "user": user}
  
  raise HTTPException(status_code=401, detail="Invalid username or password")

@auth_router.get('/me')
async def me(request: Request):
  user = get_current_user(request)
  return user


@auth_router.post("/signup")
async def signup():
    pass

@auth_router.post("/logout")
async def logout():
    pass