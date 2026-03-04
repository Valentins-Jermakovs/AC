# Imports
from pydantic import BaseModel

# ============================================
# Schema for adding a workspace project member
# ============================================
class WorkspaceProjectMemberAddSchema(BaseModel):
    project_id: str
    user_id: str
    role: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "user_id": "user_id",
                    "role": "viewer | editor | admin"
                }
            ]
        }
    }