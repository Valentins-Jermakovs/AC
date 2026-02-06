# =========================
# Token model
# =========================

# Imports
from sqlmodel import Field, SQLModel  # SQLModel base and fields
from datetime import datetime, timedelta  # Date and time handling
from ..utils.current_date import get_current_date  # Utility to get current datetime


# =========================
# Token table in database
# =========================
class Token(SQLModel, table=True):
    """
    Represents a refresh token in the database.

    Attributes:
    - id (int): Primary key, unique identifier of the token
    - user_id (int): ID of the user associated with this token (foreign key to users table)
    - refresh_token (str): The actual refresh token string
    - expires_at (datetime): Expiration date and time of the token
    - created_at (datetime): Date and time when the token was created
    """
    __tablename__ = 'tokens'

    id: int = Field(default=None, primary_key=True)  # Primary key
    user_id: int = Field(default=None, foreign_key="users.id")  # Link to user
    refresh_token: str = Field(max_length=255, index=True)  # Token string, indexed for lookup
    expires_at: datetime = Field(
        default_factory=lambda: get_current_date() + timedelta(days=7)
    )  # Default expiry: 7 days from now
    created_at: datetime = Field(default_factory=get_current_date)  # Creation timestamp
