from pydantic import BaseModel

# === pydantic modelis lietotāju autorizācijai ===
class LoginSchema(BaseModel):
    username: str
    password: str
# === === === === === === ===