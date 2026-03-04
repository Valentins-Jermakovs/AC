# Imports
from pydantic import BaseModel, Field
from typing import List
# Schemas
from app.schemas.response.workspaces.tasks.workspace_task_schema import WorkspaceTaskSchema

# Schemas
class WorkspaceTaskListSchema(BaseModel):
    items: List[WorkspaceTaskSchema] = Field(default_factory=list)