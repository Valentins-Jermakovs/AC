# Imports
from pydantic import BaseModel, field_serializer
from datetime import datetime

# =============================
# KanbanBoard schema - response
# =============================

class KanbanBoardSchema(BaseModel):
    id: str
    title: str
    createdAt: datetime

    @field_serializer("createdAt")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")