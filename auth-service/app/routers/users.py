# ===== Importi =====
from fastapi import (
    APIRouter, 
    Depends
)

from typing import Annotated
from sqlmodel import Session

from ..schemas.pagination_schema import PaginatedUsers
from ..schemas.user_schema import UserSchema

from ..services.user_read_service import (
    get_users_paginated,
    get_user_by_id, 
    get_user_by_username_or_email, 
    get_users_by_role
)

from ..dependencies.data_base_connection import get_db

# ===== Ceļa definēšana (/users) =====
router = APIRouter(prefix="/users", tags=["Users"])

# ===== Visu lietotāju izvade =====
@router.get("/",
             response_model=PaginatedUsers,
             summary="Get all users paginated",
             description="Get all users from the database"
             )
async def fetch_all_users_paginated(
        db: Annotated[Session, Depends(get_db)],
        page: int = 1,
        limit: int = 10
    ):
    return get_users_paginated(db, page, limit)

# ===== Lietotājs pēc ID =====
@router.get("/{user_id}", response_model=UserSchema,
             summary="Get user by ID",
             description="Get user by ID from the database"
             )
async def fetch_user_by_id(
        user_id: int, 
        db: Annotated[Session, Depends(get_db)]
    ):
    return get_user_by_id(user_id, db)

# ===== Lietotājs pēc vardu vai e-pasts =====
@router.get("/search/{name_or_email}", response_model=UserSchema,
             summary="Get user by username or email",
             description="Get user by username or email from the database"
             )
async def fetch_user_by_username_or_email(
        name_or_email: str, 
        db: Annotated[Session, Depends(get_db)]
    ):
    return get_user_by_username_or_email(name_or_email, db)

# ===== Lietotāju izvade pēc role =====
@router.get("/role/{role}", response_model=list[UserSchema],
             summary="Get users by role",
             description="Get users by role from the database"
             )
async def fetch_users_by_role(
        role: str, 
        db: Annotated[Session, Depends(get_db)]
    ):
    return get_users_by_role(role, db)