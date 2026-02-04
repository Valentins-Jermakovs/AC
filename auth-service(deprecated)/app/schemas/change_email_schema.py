from pydantic import BaseModel

class ChangeEmailSchema(BaseModel):
    new_email: str