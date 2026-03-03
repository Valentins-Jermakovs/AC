# Imports
from pydantic import BaseModel

# =============================
# Schema for updating a workspace project member
# =============================
class WorkspaceProjectMemberUpdateSchema(BaseModel):
    project_id: str
    user_id: str
    role: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "user_id": "user_id",
                    "role": "role"
                }
            ]
        }
    }