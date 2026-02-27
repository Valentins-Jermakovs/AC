from pydantic import BaseModel

class RoleOperationResponseSchema(BaseModel):
    updated_users: list[int]
    role_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "updated_users": [1, 2, 3],
                "role_id": 2
            }
        }
    }