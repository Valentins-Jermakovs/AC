# =========================
# Login schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation


# =========================
# User authentication input
# =========================
class LoginSchema(BaseModel):
    """
    Schema for user login.

    Attributes:
    - username (str): Username of the user
    - password (str): Password of the user
    """
    username: str
    password: str
