from pydantic import BaseModel

class WorkspaceProjectMemberAddSchema(BaseModel):
    project_id: str
    user_id: str
    role: str