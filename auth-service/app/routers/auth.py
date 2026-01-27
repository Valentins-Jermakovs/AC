# login, register, refresh
from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel


# reģistrācijas funkcionāls
from ..schemas.registration_schema import RegistrationSchema # lietotāja registrācijas shēma

# @app.post("/register")
# async def register(user: Annotated[RegistrationSchema, Form()]):
#     return user