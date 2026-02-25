from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime


class WorkspaceProjectSchema(BaseModel):
    id: str
    userId: str
    title: str
    description: Optional[str]
    createdAt: datetime

    @field_serializer("createdAt")
    def serialize_created_at(self, value: datetime):
        return value.strftime("%Y-%m-%d")