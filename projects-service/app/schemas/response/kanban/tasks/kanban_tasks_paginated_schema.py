# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from .kanban_task_schema import KanbanTaskSchema

# ============================
# PaginationMeta schema - meta
# ============================
class PaginationMetaSchema(BaseModel):
    page: int           # Current page number
    limit: int          # Number of items per page
    total_pages: int    # Total number of pages
    total_items: int    # Total number of results


# ============================
# KanbanTasksPaginated schema
# ============================
class KanbanTasksPaginatedSchema(BaseModel):
    meta: PaginationMetaSchema
    data: List[KanbanTaskSchema]