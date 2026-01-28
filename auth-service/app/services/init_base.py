from sqlmodel import SQLModel, Session, select
from .base_connection import engine
from ..models.models import Role, UserRole, User, Token

# === DB inicializators, izveido visas tabulas, ja neeksistē ===
async def init_db():
    SQLModel.metadata.create_all(engine)
# === === === === === === === === === === === === === === === ==

# === loma inicializators, izveido lomas, ja neeksistē ===
async def init_roles():
    # izveido savienojumu
    with Session(engine) as session:

        # lomu dictionary ar aprakstiem
        roles = {
            "user": "user can register and login, use system in read-only mode and write only own data",
            "admin": "administrator can register and login, use system in read-write mode and write all data"
        }

        # pārbauda, vai lomas pašlaik ir izveidotas
        existing_roles = session.exec(select(Role)).all()
        if existing_roles:
            return
        # izveido lomas, ja neeksistē
        for role_name, role_description in roles.items():
            role = Role(name=role_name, description=role_description)
            session.add(role)


        # izpilda komandu INSERT
        session.commit()
# === === === === === === === === === === === === === === === === === === === ===
        