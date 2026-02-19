# Imports
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional
# Utilities
from ..utils.current_date import get_current_date

# ========================
# PrivateTask model
# ========================
class PrivateTask(Document):
    userId: str                                                     # User ID
    title: str                                                      # Task title
    description: Optional[str] = None                               # Task description
    dueDate: Optional[datetime] = None                              # Task due date
    createdAt: datetime = Field(default_factory=get_current_date)   # Task creation date (automatically set)
    completed: bool = False                                         # Task completion status

    # Settings - indexing, sorting and collection name
    class Settings:
        name = "private_tasks"
        indexes = [
            "userId",       # Index for user ID
            "completed",    # Index for completion status
            [
                ("userId", 1),      # Compound index for user ID
                ("completed", 1),   # and completion status
                ("createdAt", -1)   # Sort by creation date in descending order
            ],
        ]

