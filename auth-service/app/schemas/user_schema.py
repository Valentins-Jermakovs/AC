from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    role: str
    active: bool
    access_token: str | None = None
    refresh_token: str | None = None
