# =========================
# Change username schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation


# =========================
# User username update input
# =========================
class ChangeUsernameSchema(BaseModel):
    """
    Schema for changing a user's username.

    Attributes:
    - new_username (str): New username to set for the user
    """
    new_username: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "new_username": "new_user_name"
            }
        }
    }
