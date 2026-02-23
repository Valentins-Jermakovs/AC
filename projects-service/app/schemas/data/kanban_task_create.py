# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskCreate schema for creating a new kanban task
# ============================================================

class KanbanTaskCreateSchema(BaseModel):
    board_id: str
    stage_id: str
    title: str
    description: Optional[str] = None