from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy import update
from ..models.models import User, Role, UserRole
from ..schemas.user_schema import UserSchema

# === lietotāju lomu maiņas funkcija ===
def change_role_for_users(
    user_ids: list[int],
    role_name: str,
    db: Session
):
    # iegūst lomu
    role_name = role_name.lower()
    role = db.exec(
        select(Role).where(Role.name == role_name)
    ).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # iegūst visus lietotājus vienā pieprasījumā
    users = db.exec(select(User).where(User.id.in_(user_ids))).all()
    # pārbaude, vai visi lietotāji eksistē
    if len(users) != len(user_ids):
        raise HTTPException(status_code=404, detail="User not found")

    # maina lomas
    for user in users:
        user_role = db.exec(
            select(UserRole).where(UserRole.user_id == user.id)
        ).first()
        if user_role:
            db.exec(
                update(UserRole)
                .where(UserRole.user_id == user.id)
                .values(role_id=role.id)
            )
        else:
            db.add(UserRole(user_id=user.id, role_id=role.id))
    db.commit() # izmainām lomas

    # atgriežams lietotājus ar jaunām lomām
    updated_users = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            Role.name.label("role")
        )
        .where(User.id.in_(user_ids))
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
    ).all()

    return [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
        for user in updated_users
    ]