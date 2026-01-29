# Šis serviss tiek izmantots lietotāja datu modifikācijai

from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User, Role, UserRole
from ..schemas.user_schema import UserSchema
from ..services.password_service import get_password_hash, verify_password

# === lietotāju datu modifikācijas funkcija (paroles maiņa) ===
def change_user_password(user_id: int, old_password: str, new_password: str, db: Session):
    # pārbaude uz lietotaja esamību
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # paroļu salīdzināšana
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # pārbaude, vai jaunā parole nesakrīt ar veco
    if old_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the old one")

    # maina paroli
    user.password_hash = get_password_hash(new_password)

    # atjaunot lietotāju
    db.commit()
    db.refresh(user)

    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    return user

# === lietotāju datu modifikācijas funkcija (lietotāja vārda maiņa) ===
def change_user_username(user_id: int, new_username: str, db: Session):
    # pārbaude uz lietotaja esamību
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # pārbaude uz esošu lietotāju
    existing_user = db.exec(
        select(User).where(User.username == new_username.lower())
    ).first()
    # ja lietotājvārds jau tiek izmantos - 400 status kods
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # maina lietotāju vārdu
    user.username = new_username.lower()

    # atjaunot lietotāju
    db.commit()
    db.refresh(user)

    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    return user

# === lietotāju datu modifikācijas funkcija (lietotāja epastu maiņa) ===
def change_user_email(user_id: int, new_email: str, db: Session):
    # pārbaude uz lietotaja esamību
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # pārbaude uz e-pasta esamību
    existing_user = db.exec(
        select(User).where(User.email == new_email.lower())
    ).first()
    # ja e-pasts jau tiek izmantots - 400 status kods
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # maina lietotāju epastu
    user.email = new_email.lower()

    # atjaunot lietotāju
    db.commit()
    db.refresh(user)

    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    return user