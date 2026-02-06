# =========================
# User activity schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation
from typing import Optional


# =========================
# User activity data
# =========================
class UserActivitySchema(BaseModel):
    """
    Schema representing user activity status.

    Attributes:
    - id (int): Unique identifier of the user
    - username (Optional[str]): Username of the user (may be None)
    - email (str): Email address of the user
    - is_active (bool): Whether the user is active (True) or inactive (False)
    """
    id: int
    username: Optional[str] = None
    email: str
    is_active: bool
