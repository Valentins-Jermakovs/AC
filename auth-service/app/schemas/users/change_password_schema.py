# =========================
# Change password schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation


# =========================
# User password update input
# =========================
class ChangePasswordSchema(BaseModel):
    """
    Schema for changing a user's password.

    Attributes:
    - old_password (str | None): Current password (optional, may be required depending on logic)
    - new_password (str): New password to set
    """
    old_password: str | None = None
    new_password: str
