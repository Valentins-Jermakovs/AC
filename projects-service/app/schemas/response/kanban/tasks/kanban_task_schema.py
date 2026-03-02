# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskSchema schema for creating a new kanban task
# ============================================================
class KanbanTaskSchema(BaseModel):
    id: str
    stageId: Optional[str] = None
    title: str
    description: Optional[str] = None
    order: Optional[float] = None