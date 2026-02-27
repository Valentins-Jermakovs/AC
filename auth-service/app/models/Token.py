# =========================
# Token model
# =========================

# Imports
# Libraries
from sqlmodel import Field, SQLModel  # SQLModel base and fields
from datetime import datetime, timedelta, timezone  # Date and time handling
# Utils
from ..utils.current_date import get_current_date  # Utility to get current datetime


# =========================
# Token table in database
# =========================
class TokenModel(SQLModel, table=True):
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


    id: int = Field(default=None, primary_key=True)         # Primary key
    user_id: int = Field(foreign_key="users.id")            # Reference to users table

    refresh_token: str = Field(                             # Refresh token
        max_length=255, 
        index=True
    )  

    expires_at: datetime = Field(                           # Expiration date
        default_factory=lambda: get_current_date() + timedelta(days=7)
    )

    created_at: datetime = Field(                           # Creation date
        default_factory=get_current_date
    ) 
