# ===== Importi =====
from sqlmodel import (
    Session, 
    select
)
from fastapi import HTTPException

from ..models.models import (
    User, 
    Role, 
    UserRole
)

from ..services.password_service import (
    get_password_hash, 
    verify_password
)

from ..schemas.user_schema import UserSchema

# ===== Lietotāja atlases funkcija =====
async def get_user_with_role (
    user_id: int, 
    db: Session
):
    user = db.exec(
        select(
            User.id,
            User.username,
            User.email,
            User.active,
            Role.name.label("role")
        )
        .join(UserRole, UserRole.user_id == User.id)
        .join(Role, Role.id == UserRole.role_id)
        .where(User.id == user_id)
    ).first()

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        active=user.active
    )


# ===== Lietotāja paroles maiņa =====
async def change_user_password(
        user_id: int, 
        old_password: str | None, # google login nevajag paroli 
        new_password: str, 
        db: Session
    ):

    # ===== Paroles politika =====
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")


    # ===== Lietotāja un paroļu pārbaude =====
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")
    
    # ===== Ja vecā parole ir None (Google autentifikācija) =====
    if user.password_hash:
        # Parole ir iestatīta
        if not old_password or not verify_password(old_password, user.password_hash):
            raise HTTPException(status_code=403, detail="Invalid password")
        if old_password == new_password:
            raise HTTPException(status_code=400, detail="New password cannot be the same as the old password")
        
    else:
        # Nav aproles, ļaujam mainīt tikai ar @gmail.com
        if not user.email.endswith("@gmail.com"):
            raise HTTPException(status_code=403, detail="User is not registered with Google")


    # ===== Paroles maiņa =====
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)


    return await get_user_with_role(user_id, db)

# ===== Lietotāja vārda maiņa =====
async def change_user_username(
        user_id: int, 
        new_username: str, 
        db: Session
    ):

    # ===== Lietotāja pārbaude =====
    user = db.get(User, user_id)

    new_username = new_username.strip().lower()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    existing_user = db.exec(
        select(User).where(User.username == new_username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.username = new_username

    # ===== Lietotātaja datu atjaunošana =====
    db.commit()
    db.refresh(user)


    return await get_user_with_role(user_id, db)

# ===== Lietotāja epasta maiņa =====
async def change_user_email(
        user_id: int, 
        new_email: str, 
        db: Session
    ):
    # ===== Lietotāja pārbaude =====
    user = db.get(User, user_id)

    new_email = new_email.strip().lower()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    existing_user = db.exec(
        select(User).where(User.email == new_email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user.email = new_email

    # ===== Lietotātaja datu atjaunošana =====
    db.commit()
    db.refresh(user)


    return await get_user_with_role(user_id, db)