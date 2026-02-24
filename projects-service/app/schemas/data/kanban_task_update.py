# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskUpdate schema for updating a kanban task
# ============================================================
class KanbanTaskUpdate(BaseModel):
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None