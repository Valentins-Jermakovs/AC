# Imports
from pydantic import BaseModel

# ============================================
# Schema for adding a workspace project member
# ============================================
class WorkspaceProjectMemberAddSchema(BaseModel):
    project_id: str
    user_id: str
    role: str