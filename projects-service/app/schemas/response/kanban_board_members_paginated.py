from pydantic import BaseModel, Field
from typing import List

from .kanban_board_member import KanbanBoardMemberSchema


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int

class KanbanBoardMembersPaginatedSchema(BaseModel):
    items: List[KanbanBoardMemberSchema] = Field(default_factory=list)
    meta: PaginationMeta