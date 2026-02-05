from pydantic import BaseModel
from typing import Optional
from typing import List

class UserSchema(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    roles: List[str]
    active: bool