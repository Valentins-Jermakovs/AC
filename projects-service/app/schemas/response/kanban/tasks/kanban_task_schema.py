# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# KanbanTaskSchema schema
# ============================================================
class KanbanTaskSchema(BaseModel):
    id: str
    stageId: Optional[str] = None
    title: str
    description: Optional[str] = None
    order: Optional[float] = None
    boardId: str