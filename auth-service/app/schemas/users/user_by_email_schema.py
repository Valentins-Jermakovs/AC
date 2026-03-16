# =========================
# User by email schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation
from typing import Optional

# =========================
# Data from backend to frontend
# =========================

class UserByEmailSchema(BaseModel):
    id: int
    email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "test@email"
            }
        }
    }