from sqlmodel import SQLModel, Session, select
from .base_connection import engine
from ..models.models import Role, UserRole, User, Token

# Izveido tabulas datu bāzē
def init_db():
    SQLModel.metadata.create_all(engine)

# funkcija, kas pievieno lomas
def init_roles():
    with Session(engine) as session:
        roles = {
            "user": "user role: user can register and login",
            "admin": "admin: user can register, login and manage users"
        }

        # if exists
        existing_roles = session.exec(select(Role)).all()
        if existing_roles:
            return

        for role_name, role_description in roles.items():
            role = Role(name=role_name, description=role_description)
            session.add(role)

        session.commit()
        