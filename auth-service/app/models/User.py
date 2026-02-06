# =========================
# User model
# =========================

# Imports
from sqlmodel import Field, SQLModel  # SQLModel base and fields
from typing import Optional
from datetime import datetime
from ..utils.current_date import get_current_date  # Utility to get current datetime


# =========================
# User table in database
# =========================
class User(SQLModel, table=True):
    """
    Represents a user in the database.

    Attributes:
    - id (int): Primary key, unique identifier of the user
    - username (str): Username, unique and indexed
    - password_hash (str): Hashed password for authentication
    - email (str): Email address, unique and indexed
    - google_id (str): Google ID if authenticated via Google
    - auth_provider (str): Authentication provider ("local" or "google")
    - created_at (datetime): Timestamp of user creation
    - active (bool): User status (active=True, banned/disabled=False)
    """
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    username: Optional[str] = Field(default=None, max_length=50, index=True, unique=True)  # Username
    password_hash: Optional[str] = Field(default=None, max_length=255)  # Hashed password
    email: str = Field(max_length=100, index=True, unique=True)  # Email
    google_id: Optional[str] = Field(default=None, index=True, unique=True)  # Google OAuth ID
    auth_provider: str = Field(default="local", max_length=20)  # Auth provider
    created_at: datetime = Field(default_factory=get_current_date)  # Creation timestamp
    active: bool = Field(default=True)  # Active status
