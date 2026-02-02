# ===== Importi =====
from sqlmodel import Session, select
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

from ..models.models import Token, User

from ..schemas.token_with_refresh_schema import TokenWithRefreshSchema

from .token_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token
)

# ===== Dotenv faila satura apstrāde =====
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# ===== Access tokena pārbaude =====
def get_user_id_from_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

# ===== Access tokena atjaunošana =====
def refresh_access_token(
    db: Session,
    refresh_token: str
) -> TokenWithRefreshSchema:

    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    expires_at = token.expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        db.delete(token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    
    # pārbaude, vai lietotājs ir aktīvs
    user = db.exec(
        select(User).where(User.id == token.user_id)
    ).first()

    if not user or not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or does not exist"
        )

    # ROTATION
    db.delete(token)
    db.commit()

    new_refresh_token = create_refresh_token()
    save_refresh_token(new_refresh_token, token.user_id, db)

    access_token = create_access_token({
        "sub": str(token.user_id)
    })

    return TokenWithRefreshSchema(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=new_refresh_token
    )
