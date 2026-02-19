# Imports
from beanie import Document

# ===========================
# Kanban Board Member Model
# ===========================
class KanbanBoardMember(Document):
    boardId: str    # Reference to the kanban board
    userId: str     # Reference to the user
    role: str       # Role of the user in the kanban board

    class Settings:
        name = "kanban_board_members"
        indexes = [
            "boardId",      # Index for board ID
            "userId",       # Index for user ID
            [
                ("boardId", 1),     # Compound index for board ID
                ("userId", 1),      # and user ID
                ("role", 1)         # and role
            ],
        ]