# demonstrējuma programma autentifikācijas pakalpojumam

# lai palaist šo programmu, instalē nepieciešamas atkarības virtuālajā vidē
# un izpildi komandu [fastapi dev main.py]
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from fastapi import Depends, Form
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from .models.models import User, Role, UserRole, Token
from .services.base_connection import engine
from .services.init_base import init_db, init_roles

# imports reģistrācijas shēmai
from .schemas.registration_schema import RegistrationSchema

# Programmas startēšana:
# izveido tabulas
# izveido lomas
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_roles()
    yield

# FastAPI servera programmas objekts
app = FastAPI(lifespan=lifespan)

# DB sesijas atkarība
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# pydantic modelis validācijai
class NewUser(BaseModel):
    username: str = Field(min_length=5, max_length=50)  # ierobežojums 3-50 simboli
    email: EmailStr                                     # automātiska e-pasta validācija
    password: str = Field(min_length=8)                 # vismaz 6 simboli

# lietotāju reģistrācija
@app.post("/register")
async def register(
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)]
):
    # veicam jaunā lietotāja validāciju
    user_date = NewUser(username=username, email=email, password=password)

    # ja lietotājs eksistē, reģistrācijas neizdevās
    existing_user = db.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # ja e-pasts eksistē, reģistrācijas neizdevās
    existing_email = db.exec(select(User).where(User.email == email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # izveido lietotāju
    user = User(
        username=user_date.username,
        email=user_date.email,
        password_hash=user_date.password
    )
    db.add(user)    # pievieno lietotāju datābāzei
    db.commit()     # saglaba lietotāju datābāzei


    # piešķir noklusējuma lomu "user"
    user_role = db.exec(select(Role).where(Role.name == "user")).first()
    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()

    return {"username": user.username, "email": user.email}     # atgriež lietotāju

# Vienkāršs saknes maršruts - tests
@app.get("/")
async def root():
    return {"message": "Hello World"}

