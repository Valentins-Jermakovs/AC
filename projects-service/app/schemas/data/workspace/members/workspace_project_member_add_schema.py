# Imports
from pydantic import BaseModel

# ============================================
# Schema for adding a workspace project member
# ============================================
class WorkspaceProjectMemberAddSchema(BaseModel):
    projectId: str
    userId: str
    role: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "userId": "userId",
                    "role": "viewer | editor | admin"
                }
            ]
        }
    }