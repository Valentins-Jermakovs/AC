# Imports
from pydantic import BaseModel

# =============================
# Schema for deleting a workspace project member
# =============================
class WorkspaceProjectMemberDeleteSchema(BaseModel):
    projectId: str
    userId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "projectId": "projectId",
                    "userId": "userId"
                }
            ]
        }   
    }