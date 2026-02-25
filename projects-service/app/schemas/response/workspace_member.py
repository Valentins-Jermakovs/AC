from pydantic import BaseModel


class WorkspaceProjectMemberSchema(BaseModel):
    project_id: str
    user_id: str
    role: str