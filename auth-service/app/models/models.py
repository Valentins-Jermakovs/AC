# ===== Importi =====
from sqlmodel import Field, SQLModel
from typing import Optional
from ..utils.datetime_utils import utcnow
from datetime import datetime, timedelta

# ===== MODEĻI =====

# ===== Lietotājs =====
class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(primary_key=True)

    username: Optional[str] = Field(
        default=None,
        max_length=50,
        index=True,
        unique=True
    )

    password_hash: Optional[str] = Field(
        default=None,
        max_length=255
    )

    email: str = Field(
        max_length=100,
        index=True,
        unique=True
    )

    google_id: Optional[str] = Field(
        default=None,
        index=True,
        unique=True
    )

    auth_provider: str = Field(
        default="local",
        max_length=20
    )

    created_at: datetime = Field(default_factory=utcnow)
    active: bool = Field(default=True)


# ===== Lomas =====
class Role(SQLModel, table=True):
    __tablename__ = 'roles'                                     

    id: int = Field(primary_key=True)
    name: str = Field(
        max_length=50, 
        unique=True, 
        index=True
    )

    description: str = Field(max_length=100)


# ===== M2M savienojums starp lietotāju un lietotāju lomu =====
class UserRole(SQLModel, table=True):
    __tablename__ = 'user_roles'

    user_id: int = Field(
        foreign_key="users.id", 
        primary_key=True
    )

    role_id: int = Field(
        foreign_key="roles.id", 
        primary_key=True
    )

# ===== Tokenu krātuve =====
class Token(SQLModel, table=True):
    __tablename__ = 'tokens'

    id: int = Field(
        default=None, 
        primary_key=True
    )           

    user_id: int = Field(
        default=None, 
        foreign_key="users.id"
    )

    refresh_token: str = Field(
        max_length=255, 
        index=True
    )

    expires_at: datetime = Field(
        default_factory=lambda: utcnow() + timedelta(days=7)
    )                     
    created_at: datetime = Field(default_factory=utcnow)                    