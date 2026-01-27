from pydantic import BaseModel

# lietotāja registrācijas formas modelis
# tiek saņemts no front-end
class RegistrationSchema(BaseModel):
    username: str
    email: str
    password: str