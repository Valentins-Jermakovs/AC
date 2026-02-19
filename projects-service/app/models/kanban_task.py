# Imports
from datetime import datetime
from typing import Optional
from pydantic import Field
# Utilities
from ..utils.current_date import get_current_date

# ========================
# KanbanTask model
# ========================
class KanbanTask:
    boardId: str    # Board ID
    stageId: str    # Stage ID

    title: str                          # Task title
    description: Optional[str] = None   # Task description
    order: int                          # Task order

    class Settings:
        name = "kanban_tasks"
        indexes = [
            "boardId",      # Index for board ID
            "stageId",      # Index for stage ID
            [
                ("boardId", 1),     # Compound index for board ID
                ("stageId", 1),     # and stage ID
                ("order", -1)       # Sort by order in descending order
            ],
        ]