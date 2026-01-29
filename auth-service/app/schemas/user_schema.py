from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    role: str