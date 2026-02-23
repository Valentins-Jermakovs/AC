# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .kanban_board import KanbanBoardSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int

# ============================
# KanbanBoardsPaginated schema
# ============================
class KanbanBoardsPaginatedSchema(BaseModel):
    items: List[KanbanBoardSchema] = Field(default_factory=list)
    meta: PaginationMeta