# =========================
# Pagination schema for users
# =========================

# Imports
from pydantic import BaseModel  # Pydantic base model for validation
from typing import List
from ..users.user_schema import UserSchema  # User schema for individual user entries


# =========================
# Pagination metadata
# =========================
class PaginationMeta(BaseModel):
    """
    Metadata for paginated results.

    Attributes:
    - page (int): Current page number
    - limit (int): Number of items per page
    - total_users (int): Total number of users in the database
    - total_pages (int): Total number of pages available
    """
    page: int
    limit: int
    total_users: int
    total_pages: int


# =========================
# Paginated users response
# =========================
class PaginatedUsers(BaseModel):
    """
    Schema for returning paginated list of users.

    Attributes:
    - items (List[UserSchema]): List of users on the current page
    - meta (PaginationMeta | None): Pagination metadata (optional)
    """
    items: List[UserSchema]
    meta: PaginationMeta | None = None
