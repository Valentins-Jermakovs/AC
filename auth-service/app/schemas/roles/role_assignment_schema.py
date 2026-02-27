# Imports
from pydantic import BaseModel

# ========================
# Role assignment schema
# ========================
class RoleAssignmentSchema(BaseModel):
    user_ids: list[int]
    role_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_ids": [1, 2, 3],
                "role_id": 2
            }
        }
    }