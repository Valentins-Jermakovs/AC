# Imports
from pydantic import BaseModel

# =============================
# KanbanBoardMember schema - response
# =============================
class KanbanBoardMemberSchema(BaseModel):
    userId: str
    boardId: str
    role: str