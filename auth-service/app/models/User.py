# Imports
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from ..utils.current_date import get_current_date

# User model
# This class represents a user in the database
#
# Attributes:
# - id (int): The unique identifier for the user.
# - username (str): The username of the user.
# - password_hash (str): The hashed password of the user.
# - email (str): The email address of the user.
# - google_id (str): The Google ID of the user.
# - auth_provider (str): The authentication provider of the user.
# - created_at (datetime): The date and time the user was created.
# - active (bool): Whether the user is active or not (banned or not).

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(primary_key=True)
    username: Optional[str] = Field(default=None, max_length=50, index=True, unique=True)
    password_hash: Optional[str] = Field(default=None, max_length=255)
    email: str = Field(max_length=100, index=True, unique=True)
    google_id: Optional[str] = Field(default=None, index=True, unique=True)
    auth_provider: str = Field(default="local", max_length=20)
    created_at: datetime = Field(default_factory=get_current_date)
    active: bool = Field(default=True)