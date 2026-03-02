# Imports
from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional
# Utilities
from ..utils.current_date import get_current_date

'''
Kanban models

- KanbanBoardModel: describe a kanban board
- KanbanStageModel: describe a kanban stage
- KanbanTaskModel: describe a kanban task
- KanbanBoardMemberModel: describe a kanban board member

Models are used to define the structure of the data stored in the database, 
and can be used to validate the data before it is saved.
'''

# ===========================
# Kanban Board Member Model
# ===========================
class KanbanBoardMemberModel(Document):
    boardId: str    # Reference to the kanban board
    userId: str     # Reference to the user
    role: str       # Role of the user

    class Settings:
        name = "kanban_board_members"
        indexes = [
            "boardId",      # Index for board ID
            "userId",       # Index for user ID
            "role",         # Index for role
            [
                ("boardId", 1),     # Compound index for board ID
                ("userId", 1),      # and user ID
                ("role", 1)         # and role
            ],
        ]

# ========================
# KanbanBoard model
# ========================
class KanbanBoardModel(Document):
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


# ========================
# KanbanTask model
# ========================
class KanbanTaskModel(Document):
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