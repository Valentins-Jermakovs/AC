# Imports
from datetime import datetime
from pydantic import Field
from beanie import Document
# Utilities
from ..utils.current_date import get_current_date

# ========================
# KanbanStage model
# ========================
class KanbanStageModel(Document):
    boardId: str    # Foreign key to the KanbanBoard model
    title: str      # Stage title
    order: float    # Stage order
    createdAt: datetime = Field(default_factory=get_current_date)   # Creation date (auto-generated)

    class Settings:
        name = "kanban_stages"
        indexes = [
            "boardId",      # Index for board ID
            [
                ("boardId", 1),     # Compound index for board ID
                ("order", 1),       # and order
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]