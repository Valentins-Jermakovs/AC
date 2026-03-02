# Imports
from pydantic import BaseModel, Field
from typing import List
# Models
from app.schemas.response.kanban.members.kanban_board_member_schema import KanbanBoardMemberSchema

# ===============================
# PaginationMeta schema - meta
# ===============================
class PaginationMetaSchema(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int

#  ================================
# KanbanBoardMembersPaginated schema - response
# ================================
class KanbanBoardMembersPaginatedSchema(BaseModel):
    items: List[KanbanBoardMemberSchema] = Field(default_factory=list)
    meta: PaginationMetaSchema