# Imports
from typing import Optional
from pydantic import BaseModel

# ============================================================
# PrivateTaskCreateData schema for creating a new private task
# ============================================================
class PrivateTaskCreateSchema(BaseModel):
    title: str                          # Task title
    description: Optional[str] = None   # Task description
    dueDate: Optional[str] = None       # Task due date