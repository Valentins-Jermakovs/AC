# Imports
from pydantic import BaseModel
from typing import Optional

# =============================
# WorkspaceTaskSchema schema - response
# =============================
class WorkspaceTaskSchema(BaseModel):
    id: str
    projectId: str
    stageId: str
    title: str
    description: Optional[str] = None
    storyPoints: Optional[int] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    createdAt: str
    dueDate: Optional[str]