# Imports
from pydantic import BaseModel
from ..schemas.user_schema import UserSchema

# pydantic model for change role response
class ChangeRoleResponseSchema(BaseModel):
    users: list[UserSchema]