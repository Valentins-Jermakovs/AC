# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from app.schemas.response.kanban.boards.kanban_board_schema import KanbanBoardSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMetaSchema(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int

# ============================
# KanbanBoardsPaginated schema
# ============================
class KanbanBoardsPaginatedSchema(BaseModel):
    items: List[KanbanBoardSchema] = Field(default_factory=list)
    meta: PaginationMetaSchema