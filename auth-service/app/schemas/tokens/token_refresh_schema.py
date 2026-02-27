# =========================
# Token refresh schema
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation


# =========================
# Token response
# =========================
class TokenRefreshSchema(BaseModel):
    """
    Schema for returning access and refresh tokens.

    Attributes:
    - access_token (str): JWT access token
    - token_type (str): Token type (e.g., "Bearer")
    - refresh_token (str): Refresh token for generating new access tokens
    """
    access_token: str
    token_type: str
    refresh_token: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }
    }
