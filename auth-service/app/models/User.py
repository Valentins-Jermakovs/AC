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

    id: Optional[int] = Field(              # Primary key
        default=None, 
        primary_key=True
    )  
    username: Optional[str] = Field(        # Username
        default=None, 
        max_length=50, 
        index=True, 
        unique=True
    )  
    password_hash: Optional[str] = Field(   # Hashed password
        default=None,
        max_length=255
    )  
    email: str = Field(                     # Email
        max_length=100, 
        index=True, 
        unique=True
    )  
    google_id: Optional[str] = Field(       # Google OAuth ID
        default=None, 
        index=True, 
        unique=True
    )  
    auth_provider: str = Field(             # Auth provider
        default="local", 
        max_length=20
    )  
    created_at: datetime = Field(           # Creation timestamp
        default_factory=get_current_date
    )  
    active: bool = Field(                   # User status
        default=True
    )  
