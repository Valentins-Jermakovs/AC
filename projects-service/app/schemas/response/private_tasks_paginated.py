# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .private_task import PrivateTaskSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMeta(BaseModel):
    page: int           # Current page number
    limit: int          # Number of items per page
    total_pages: int    # Total number of pages
    total_results: int  # Total number of results

# ============================
# PaginatedPrivateTasks schema
# ============================
class PaginatedPrivateTasks(BaseModel):
    items: List[PrivateTaskSchema] = Field(default_factory=list)    # List of private tasks
    meta: PaginationMeta                                            # Pagination metadata