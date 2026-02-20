# Imports
from typing import Optional
from pydantic import BaseModel, field_serializer
from datetime import datetime

# =============================
# PrivateTask schema - response
# =============================
class PrivateTaskSchema(BaseModel):
    id: str                             # Task ID
    title: str                          # Title
    description: Optional[str] = None   # Description
    createdAt: datetime                 # Creation date
    dueDate: Optional[datetime] = None  # Due date
    completed: bool                     # Completion status
    
    # Serializers
    @field_serializer("createdAt")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")
    
    @field_serializer("dueDate")
    def serialize_due_date(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime("%Y-%m-%d") if value else None
    
    @field_serializer("id")
    def serialize_id(self, value):
        return str(value)