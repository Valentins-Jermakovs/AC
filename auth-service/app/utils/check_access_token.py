# Imports
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os


# dotenv file contents read
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Access token check
async def check_access_token(access_token: str) -> int:

    # Token decode
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
        

    # Error handling
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    # Error handling
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )