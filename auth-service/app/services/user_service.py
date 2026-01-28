from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User, Role, UserRole
from ..schemas.registration_schema import RegistrationSchema

async def register_user(data: RegistrationSchema, db: Session):

    # === validācija ===
    # pārbaudes uz esošu lietotāju
    existing_user = db.exec(
        select(User).where(User.username == data.username)
    ).first()
    # ja lietotājvārds jau tiek izmantos - 400 status kods
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    existing_email = db.exec(select(User).where(User.email == data.email)).first()
    # ja epasts jau tiek izmantots - 400 status kods
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    # === === === === ===

    # === jaunā lietotāja objekta veidošana ===
    user = User(
        username=data.username,
        email=data.email,
        password_hash=data.password
    )
    # === === === === === === === === === ===


    # === pievieno lietotāju ===
    db.add(user)        # pievieno lietotāja objektu SQLAlchemy/SQLModel sesijai
    db.commit()         # izpilda komandu INSERT
    db.refresh(user)    # izvelk izveidotu lietotāju no DB pēc ID
    # === === === === === ===

    # === pievieno lietotājam lomu (user) ===
    # atrod lietotāju lomu - user
    user_role = db.exec(
        select(Role).where(Role.name == "user")
    ).first()
    # pievieno jaunajam lietotājam lomu pēc noklusējuma (user)
    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()
    # === === === === === === === === === === ===

    # atgriež lietotāja objektu
    return user
