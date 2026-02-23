# Imports
from pydantic import BaseModel

# ============================================================
# KanbanBoardCreate schema for creating a new kanban board
# ============================================================
class KanbanBoardUpdateSchema(BaseModel):
    board_id: str  # Kanban board ID
    title: str     # Kanban board title