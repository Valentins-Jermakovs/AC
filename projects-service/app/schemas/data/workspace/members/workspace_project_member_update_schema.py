# Imports
from pydantic import BaseModel

# =============================
# Schema for updating a workspace project member
# =============================
class WorkspaceProjectMemberUpdateSchema(BaseModel):
    projectId: str
    userId: str
    role: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "userId": "userId",
                    "role": "role"
                }
            ]
        }
    }