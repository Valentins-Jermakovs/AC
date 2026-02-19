# Imports
from datetime import datetime
from pydantic import Field
# Utilities
from ..utils.current_date import get_current_date

# ========================
# KanbanBoard model
# ========================
class KanbanBoard:
    userId: str                                                      # User ID
    title: str                                                       # Board title
    createdAt: datetime = Field(default_factory=get_current_date)    # Creation date (automatically set)

    class Settings:
        name = "kanban_boards"
        indexes = [
            "userId",               # Index for user ID
            [
                ("userId", 1),      # Compound index for user ID
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]