# Imports
from pydantic import BaseModel, field_serializer

# =============================
# KanbanBoardMember schema - response
# =============================

class KanbanBoardMemberSchema(BaseModel):
    userId: str
    boardId: str
    role: str