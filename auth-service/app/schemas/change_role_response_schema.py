# Imports
from pydantic import BaseModel
from ..schemas.user_schema import UserSchema

# pydantic model for change role response
class ChangeRoleResponseSchema(BaseModel):
    users: list[UserSchema]
    access_token: str | None = None     # new access token
    refresh_token: str | None = None    # new refresh token