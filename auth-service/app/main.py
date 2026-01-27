# demonstrējuma programma autentifikācijas pakalpojumam

# lai palaist šo programmu, instalē nepieciešamas atkarības virtuālajā vidē
# un izpildi komandu [fastapi dev main.py]

from fastapi import FastAPI
from pydantic import BaseModel

from sqlmodel import Session, select, SQLModel
from .models.models import User, Role, UserRole, Token
from .services.base_connection import engine
from .services import init_base

app = FastAPI()

# DB sesijas atkarība
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Vienkāršs saknes maršruts - tests
@app.get("/")
async def root():
    return {"message": "Hello World"}

