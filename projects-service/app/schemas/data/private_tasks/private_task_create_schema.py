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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "New task",
                    "description": "New task description",
                    "dueDate": "2023-01-01"
                }
            ]
        }
    }