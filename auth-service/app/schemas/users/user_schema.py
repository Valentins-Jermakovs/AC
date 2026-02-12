# =========================
# User schema
# =========================

# Imports
from pydantic import BaseModel, field_serializer  # Pydantic base model for validation
from typing import Optional, List
from datetime import datetime


# =========================
# User data
# =========================
class UserSchema(BaseModel):
    """
    Schema representing a user.

    Attributes:
    - id (int): Unique identifier of the user
    - username (Optional[str]): Username of the user (may be None)
    - email (str): Email address of the user
    - roles (List[str]): List of role names assigned to the user
    - active (bool): Whether the user is active (True) or inactive (False)
    """
    id: int
    username: Optional[str] = None
    email: str
    roles: List[str]
    created_at: datetime
    active: bool

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return value.strftime("%Y-%m-%d")
