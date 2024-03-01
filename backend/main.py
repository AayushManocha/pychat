from app.controllers.auth import auth_router
from app.controllers.message import message_router 
from app.server import app
import uvicorn
from app.database.db import clear_db, create_db, seed_db

def start_app():
    create_db()
    clear_db()
    seed_db()

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_app()