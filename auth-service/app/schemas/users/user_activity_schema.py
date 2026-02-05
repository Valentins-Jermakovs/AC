from pydantic import BaseModel
from typing import Optional

class UserActivitySchema(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    is_active: bool