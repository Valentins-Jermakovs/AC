# Šis serviss atbilsts par lietotāju aktivitātes statusa maiņu

from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User
from ..schemas.user_active_schema import UserActiveSchema

# === lietotāju aktivitātes statusa maiņas funkcija ===
def change_users_activity_status(
    user_ids: list[int],
    is_active: bool,
    db: Session
):
    # iegūst visus lietotājus vienā pieprasījumā
    users = db.exec(
        select(User).where(User.id.in_(user_ids))).all()
    # pārbaude, vai visi lietotāji eksistē
    if len(users) != len(user_ids):
        raise HTTPException(status_code=404, detail="User not found")

    # maina aktivitātes statusu
    for user in users:
        user.active = is_active

    db.commit()
    return [
        UserActiveSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.active
        )
        for user in users
    ]