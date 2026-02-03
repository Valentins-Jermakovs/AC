# ===== Importi =====
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os

from ..models.models import User, Role, UserRole

from ..dependencies.data_base_connection import get_db

# ===== Dotenv faila satura apstrāde =====
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        # meklē lietotāju
        user = db.exec(
            select(User).where(User.id == int(user_id))
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return user
        

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
    

