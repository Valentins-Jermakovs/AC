# =========================
# User activity schemas
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation
from typing import Optional


# =========================
# User activity data
# =========================
class UserActivitySchemaData(BaseModel):
    """
    Schema representing user activity status.

    Attributes:
    - user_ids (list[int]): List of user IDs
    - is_active (bool): Whether the user is active (True) or inactive (False)
    """
    user_ids: list[int]
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_ids": [1, 2, 3],
                "is_active": True
            }
        }
    }

# =========================
# User activity response
# =========================
class UserActivitySchemaResponse(BaseModel):
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
