# Imports
from pydantic import BaseModel, Field, EmailStr

# pydantic model for user registration
class RegistrationSchema(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr                              
    password: str = Field(min_length=8)
