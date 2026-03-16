# Imports
from pydantic import BaseModel

# =============================
# KanbanBoardMember schema - response
# =============================
class KanbanBoardMemberSchema(BaseModel):
    email: str
    userId: str
    boardId: str
    role: str