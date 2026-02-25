from pydantic import BaseModel
from typing import Optional


class WorkspaceProjectCreateSchema(BaseModel):
    title: str
    description: Optional[str]
    # userId would be fetched from token