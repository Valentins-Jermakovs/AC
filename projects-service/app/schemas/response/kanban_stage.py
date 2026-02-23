from pydantic import BaseModel, field_serializer
from datetime import datetime

# =============================
# KanbanStage schema - response
# =============================
class KanbanStageSchema(BaseModel):
    id: str
    title: str
    order: float
    createdAt: datetime

    @field_serializer("createdAt")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")