# Imports
from pydantic import BaseModel

# pydantic model for token refresh
class TokenRefreshSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
