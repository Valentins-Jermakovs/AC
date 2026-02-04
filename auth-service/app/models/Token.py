# Imports
from sqlmodel import Field, SQLModel
from datetime import datetime, timedelta
from ..utils.current_date import get_current_date

# Token model
# This class represents a token in the database
#
# Attributes:
# - id (int): The unique identifier for the token.
# - user_id (int): The ID of the user associated with the token.
# - refresh_token (str): The refresh token for the token.
# - expires_at (datetime): The expiration date and time of the token.
# - created_at (datetime): The date and time the token was created.

class Token(SQLModel, table=True):
    __tablename__ = 'tokens'

    id: int = Field(default=None, primary_key=True)           
    user_id: int = Field(default=None, foreign_key="users.id")
    refresh_token: str = Field(max_length=255, index=True)
    expires_at: datetime = Field(default_factory=lambda: get_current_date() + timedelta(days=7))                     
    created_at: datetime = Field(default_factory=get_current_date)    