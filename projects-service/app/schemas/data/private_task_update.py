# Imports
from pydantic import BaseModel
from typing import Optional

# ===========================================================
# PrivateTaskUpdate schema for updating a private task
# ===========================================================
class PrivateTaskUpdateSchema(BaseModel):
    title: Optional[str] = None         # Task title
    description: Optional[str] = None   # Task description
    dueDate: Optional[str] = None       # Task due date
    completed: Optional[bool] = None    # Task completion