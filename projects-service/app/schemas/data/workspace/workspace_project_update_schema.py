# Imports
from pydantic import BaseModel
from typing import Optional

# ============================================================
# WorkspaceProjectUpdate schema for updating a workspace project
# ============================================================
class WorkspaceProjectUpdateSchema(BaseModel):
    project_id: str
    title: str
    description: Optional[str]