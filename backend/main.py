from app.controllers.auth import auth_router
from app.controllers.message import message_router 
from app.server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)