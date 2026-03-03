# Imports
from pydantic import BaseModel

# =============================
# Schema for deleting a workspace project member
# =============================
class WorkspaceProjectMemberDeleteSchema(BaseModel):
    project_id: str
    user_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "user_id": "user_id"
                }
            ]
        }   
    }