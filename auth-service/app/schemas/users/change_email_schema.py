# =========================
# Change email schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation


# =========================
# User email update input
# =========================
class ChangeEmailSchema(BaseModel):
    """
    Schema for changing a user's email.

    Attributes:
    - new_email (str): New email address to set for the user
    """
    new_email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "new_email": "new@email.com"
            }
        }
    }