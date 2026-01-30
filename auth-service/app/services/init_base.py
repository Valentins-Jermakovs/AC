# ===== Importi =====
from sqlmodel import (
    SQLModel, 
    Session, 
    select, 
    create_engine
)
import os
from dotenv import load_dotenv

from ..models.models import (
    Role, 
    UserRole, 
    User, 
    Token
)

# ===== Dotenv faila satura apstrāde =====
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


# ===== DB tabulu inicializācija =====
async def init_db():
    SQLModel.metadata.create_all(engine)


# ===== Lomu inicializācija =====
async def init_roles():

    with Session(engine) as session:

        # Lomas
        roles = {
            "user": "user can register and login, use system in read-only mode and write only own data",
            "admin": "administrator can register and login, use system in read-write mode and write all data"
        }

        # Pārbaude
        existing_roles = session.exec(select(Role)).all()

        if existing_roles:
            return

        # Izveido lomas
        for role_name, role_description in roles.items():
            role = Role(name=role_name, description=role_description)
            session.add(role)

        session.commit()
