from pydantic import BaseModel

class TokenWithRefreshSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
