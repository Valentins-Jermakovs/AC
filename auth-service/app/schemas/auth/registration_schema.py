# =========================
# Registration schema
# =========================

# Imports
from pydantic import BaseModel, Field, EmailStr  # Pydantic base, field validation, and email type


# =========================
# User registration input
# =========================
class RegistrationSchema(BaseModel):
    """
    Schema for registering a new user.

    Attributes:
    - username (str): Username, 5-50 characters
    - email (EmailStr): User email address, validated as proper email
    - password (str): Password, minimum 8 characters
    """
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
