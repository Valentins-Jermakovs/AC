# Šis serviss atbild par lietotāju mekēšanu/atlasi

from sqlmodel import Session, select
from sqlalchemy import or_
from fastapi import HTTPException
from ..models.models import User, Role, UserRole
from ..schemas.user_schema import UserSchema


# === izvada visus lietotājus no DB ===
def get_all_users(db: Session) -> list[User]:
    return db.exec(select(User)).all()

# === meklē lietotāju pēc ID ===
def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# === === === === === === === === === === === === === === === ===

# meklē lietotāju pēc username vai email
def get_user_by_username_or_email(username_or_email: str, db: Session) -> User:
    user = db.exec(
        select(User)
        .where(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        )
    ).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# === === === === === === === === === === === === === === === ===

# meklē lietotājus pēc role
def get_users_by_role(role: str, db: Session) -> list[User]:
    users = db.exec(
        select(User)
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(Role.name == role)
    ).all()
    return users
# === === === === === === === === === === === === === === === ===