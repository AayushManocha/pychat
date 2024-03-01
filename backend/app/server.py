from fastapi import FastAPI
from app.controllers.auth import auth_router
from app.controllers.message import message_router 
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.chat import chat_router
from app.controllers.user import user_router

origins = [
    "http://localhost:5173",  # Allow localhost for development
]

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(message_router)
app.include_router(chat_router)
app.include_router(user_router)