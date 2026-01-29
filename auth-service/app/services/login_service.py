# === Serviss lietotāju autentifikācijai ===
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import User, Token
from ..schemas.auth_schema import LoginSchema
from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema
from ..services.password_service import verify_password
from ..services.token_servicce import create_access_token, create_refresh_token, save_refresh_token
from datetime import datetime, timedelta, timezone
from ..utils.datetime_utils import utcnow

# === lietotāju autentifikāciajs funkcija ===
def login_user(db: Session, data: LoginSchema) -> TokenWithRefreshSchema:

    # username uz lowercase
    data.username = data.username.lower()

    # === pārbaudes uz esošu lietotāju ===
    user = db.exec(
        select(User).where(User.username == data.username)
    ).first()
    # === ja lietotājs neeksistē - 401 status kods ===
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # paroles salīdzināšana
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")
    # ja lietotājs ir nav aktvīs - 401 status kods
    if not user.active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # === access tokena ģenerāciuja ===
    access_token = create_access_token({"sub": str(user.id),})

    # === pārbaude uz refresh tokenu DB ===
    # atrodam refresh tokenu datu bāzē
    token = db.exec(
        select(Token)
        .where(Token.user_id == user.id)
        .order_by(Token.created_at.desc())
    ).first()
    # ja refsresh_tokens eksistē, veicam pārbaudi uz tā derīgumu
    if token:
        if token.expires_at.replace(tzinfo=timezone.utc) < utcnow():
            # ja beidzies, dzēšam
            db.delete(token)
            db.commit()
            token = None

    # ja refresh tokena nav, veidojam
    if not token:
        refresh_token_value = create_refresh_token()
        # saglabā refresh tokenu DB
        save_refresh_token(refresh_token_value, user.id, db)
    else:
        refresh_token_value = token.refresh_token
    # === === === === === === === === === === === ===

    # atgriež tokenu un refresh tokenu
    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token_value
    )
