# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskSchema schema for creating a new kanban task
# ============================================================
class KanbanTaskSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None