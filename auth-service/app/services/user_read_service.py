# ===== Importi =====
from sqlmodel import Session, select
from sqlalchemy import or_
from fastapi import HTTPException

from ..models.models import (
    User, 
    Role, 
    UserRole
)

from ..schemas.user_schema import UserSchema
from ..schemas.pagination_schema import PaginatedUsers, PaginationMeta

# ===== Visu lietotaju atlase (paginated) =====
def get_users_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    # ===== Paginācija =====
    offset = (page - 1) * limit

    # ===== Kopējs lietotāju skaits =====
    total_users = db.exec(
        select(User)
    ).all()

    total_users = len(total_users)

    # ===== Paginācija pārbaude =====
    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # ===== Visu lietotaju atlase =====
    users = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .limit(limit)
        .offset(offset)
    ).all()

    # ===== User -> UserSchema =====
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            active=user.active
        )
        for user in users
    ]

    # ===== Meta informācija =====
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )
    

    return PaginatedUsers(items=items, meta=meta)


# ===== Lietotājs pēc ID =====
def get_user_by_id(user_id: int, db: Session) -> UserSchema:

    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        active=user.active
    )

# ===== Lietotājs pēc username vai email =====
def get_user_by_username_or_email(
        username_or_email: str, 
        db: Session,
        page: int = 1,
        limit: int = 10
    ) -> PaginatedUsers:

    # ===== Paginācija =====
    offset = (page - 1) * limit

    username_or_email = username_or_email.strip().lower()

    users = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(
            or_(
                User.username.ilike(f"%{username_or_email}%"),
                User.email.ilike(f"%{username_or_email}%")
            )
        )
    ).all()

    if users == []:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ===== Kopējs lietotāju skaits =====
    total_users = len(users)

    # ===== Paginācija pārbaude =====
    if offset >= len(users):
        raise HTTPException(status_code=404, detail="Page not found")
    
    # ===== User -> UserSchema =====
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            active=user.active
        )
        for user in users[offset:offset + limit]
    ]

    # ===== Meta informācija =====
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)

# ===== Visu lietotāju atlase pēc role =====
def get_users_by_role(
        role: str, 
        db: Session,
        page: int = 1,
        limit: int = 10
    ) -> PaginatedUsers:

    role = role.strip().lower()

    users = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(Role.name == role)
    ).all()

    if users == []:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # ===== Kopējs lietotāju skaits =====
    total_users = len(users)

    # ===== Paginācija pārbaude =====
    offset = (page - 1) * limit
    if offset >= len(users):
        raise HTTPException(status_code=404, detail="Page not found")
    
    # ===== User -> UserSchema =====
    items = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            active=user.active
        )
        for user in users[offset:offset + limit]
    ]

    # ===== Meta informācija =====
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)