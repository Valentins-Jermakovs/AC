from pydantic import BaseModel


class UserReadResponseSchema(BaseModel):
    users: list
    access_token: str | None = None
    refresh_token: str | None = None