from fastapi import FastAPI
from app.controllers.auth import auth_router
from app.controllers.message import message_router 


app = FastAPI()

app.include_router(auth_router)
app.include_router(message_router)