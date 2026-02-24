# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .kanban_task import KanbanTaskSchema

# ============================
# PaginationMeta schema - meta
# ============================

class PaginationMeta(BaseModel):
    page: int           # Current page number
    limit: int          # Number of items per page
    total_pages: int    # Total number of pages
    total_items: int  # Total number of results


# ============================
# KanbanTasksPaginated schema
# ============================

class KanbanTasksPaginated(BaseModel):
    meta: PaginationMeta
    data: List[KanbanTaskSchema]