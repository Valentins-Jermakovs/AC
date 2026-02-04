from pydantic import BaseModel, Field, EmailStr
# === pydantic modelis validācijai - jaunā lietotāja reģistrācija ===
class RegistrationSchema(BaseModel):
    username: str = Field(min_length=5, max_length=50)  # ierobežojums 3-50 simboli
    email: EmailStr                                     # automātiska e-pasta validācija
    password: str = Field(min_length=8)                 # vismaz 6 simboli
# === === === === === === === === === === === === === === === === === === === ===