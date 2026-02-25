from pydantic import BaseModel
from typing import Optional


class WorkspaceProjectUpdateSchema(BaseModel):
    project_id: str
    title: str
    description: Optional[str]