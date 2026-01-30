from pydantic import BaseModel
from typing import List

from ..schemas.user_schema import UserSchema

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_users: int
    total_pages: int

class PaginatedUsers(BaseModel):
    items: List[UserSchema]
    meta: PaginationMeta