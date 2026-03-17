# Imports
from pydantic import BaseModel

# ============================
# WorkspaceMember schema - response
# ============================
class WorkspaceProjectMemberSchema(BaseModel):
    projectId: str
    userId: str
    role: str
    email: str