# Imports
from pydantic import BaseModel

# pydantic model for user authentication
class LoginSchema(BaseModel):
    username: str
    password: str