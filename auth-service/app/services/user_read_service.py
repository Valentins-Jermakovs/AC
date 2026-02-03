# Imports
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


'''
===== User Service Documentation =====

This module provides functions for retrieving users from the database, supporting pagination, searching, and filtering by role. 
All returned users include their associated role.

Functions:

1. get_users_paginated(db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers
   - Purpose: Retrieve all users with pagination.
   - Input: database session, page number, limit per page.
   - Output: PaginatedUsers object containing list of UserSchema and pagination metadata.
   - Errors: 404 if requested page does not exist.

2. get_user_by_id(user_id: int, db: Session) -> UserSchema
   - Purpose: Retrieve a single user by ID.
   - Input: user ID, database session.
   - Output: UserSchema object with user info and role.
   - Errors: 404 if user not found.

3. get_user_by_username_or_email(username_or_email: str, db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers
   - Purpose: Retrieve users by partial match of username or email with pagination.
   - Input: search string, database session, page, limit.
   - Output: PaginatedUsers with matching users and pagination info.
   - Errors: 404 if no users match or page does not exist.

4. get_users_by_role(role: str, db: Session, page: int = 1, limit: int = 10) -> PaginatedUsers
   - Purpose: Retrieve users filtered by role with pagination.
   - Input: role name, database session, page, limit.
   - Output: PaginatedUsers with users of specified role and pagination info.
   - Errors: 404 if no users with the role exist or page does not exist.

All functions return users as UserSchema:
  id: int
  username: str
  email: str
  role: str
  active: bool

Pagination metadata returned in PaginatedUsers:
  page: int
  limit: int
  total_users: int
  total_pages: int

Notes:
- Pagination is 1-indexed.
- Role info is included via join with UserRole and Role tables.
- Search is case-insensitive for username and email.
- Raises HTTPException with 404 when invalid input or empty results occur.
'''


# All users paginated
async def get_users_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    # Offset - pagination
    offset = (page - 1) * limit

    total_users = db.exec(
        select(User)
    ).all()

    total_users = len(total_users)

    # Check if page exists
    if offset >= total_users:
        raise HTTPException(status_code=404, detail="Page not found")

    # All users
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

    # User -> UserSchema
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

    # Meta
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )
    

    return PaginatedUsers(items=items, meta=meta)


# User by ID
async def get_user_by_id(
    user_id: int, 
    db: Session
) -> UserSchema:

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

# User by username or email
async def get_user_by_username_or_email(
    username_or_email: str, 
    db: Session,
    page: int = 1,
    limit: int = 10
) -> PaginatedUsers:

    # Offset - pagination
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
    
    total_users = len(users)

    # Check if page exists
    if offset >= len(users):
        raise HTTPException(status_code=404, detail="Page not found")
    
    # User -> UserSchema
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

    # Meta
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)

# Users by role
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
    
    total_users = len(users)

    # Check if page exists
    offset = (page - 1) * limit
    if offset >= len(users):
        raise HTTPException(status_code=404, detail="Page not found")
    
    # User -> UserSchema
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

    # Meta
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total_users=total_users,
        total_pages=(total_users + limit - 1) // limit
    )

    return PaginatedUsers(items=items, meta=meta)