# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardCreate schema for creating a new kanban board
# ============================================================
class KanbanBoardCreateSchema(BaseModel):
    title: str  # Kanban board title