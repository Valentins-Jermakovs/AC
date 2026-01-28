from pydantic import BaseModel

# === pydantic modelis tokenam ===
class TokenSchema(BaseModel):
    access_token: str
    token_type: str
# === === === === === === === === ===