# Šis fails atbils par read operācijām (lietotāju mekēšanu/atlasi)
from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session

from ..schemas.user_schema import UserSchema
from ..services.user_read_service import get_all_users, get_user_by_id, get_user_by_username_or_email, get_users_by_role
from ..services.base_connection import engine

# === definē ceļu /users ===
router = APIRouter(prefix="/users", tags=["Users"])

# === veidojam savienojumu ar DB ===
def get_db():                   # veido savienojumu ar DB
    session = Session(engine)   # izveido savienojumu
    try:                        # izmanto savienojumu
        yield session
    finally:                    # izslēdz savienojumu
        session.close()

# === izvada visus lietotājus no DB ===
@router.get("/", response_model=list[UserSchema],
             summary="Get all users",
             description="Get all users from the database"
             )
async def fetch_all_users(db: Annotated[Session, Depends(get_db)]):
    return get_all_users(db)

# === izvada lietotāju pēc ID ===
@router.get("/{user_id}", response_model=UserSchema,
             summary="Get user by ID",
             description="Get user by ID from the database"
             )
async def fetch_user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return get_user_by_id(user_id, db)

# === izvada lietotāju pēc username vai email ===
@router.get("/search/{name_or_email}", response_model=UserSchema,
             summary="Get user by username or email",
             description="Get user by username or email from the database"
             )
async def fetch_user_by_username_or_email(name_or_email: str, db: Annotated[Session, Depends(get_db)]):
    return get_user_by_username_or_email(name_or_email, db)

# === izvada lietotājus pēc role ===
@router.get("/role/{role}", response_model=list[UserSchema],
             summary="Get users by role",
             description="Get users by role from the database"
             )
async def fetch_users_by_role(role: str, db: Annotated[Session, Depends(get_db)]):
    return get_users_by_role(role, db)