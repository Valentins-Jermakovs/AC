from pydantic import BaseModel

class ChangePasswordSchema(BaseModel):
    old_password: str | None = None
    new_password: str