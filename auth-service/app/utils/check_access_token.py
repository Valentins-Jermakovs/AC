# =========================
# Token validation utility
# =========================

# FastAPI exceptions and HTTP status codes
from fastapi import HTTPException, status
# JWT handling (decode tokens and catch errors)
from jose import jwt, JWTError, ExpiredSignatureError
# Load environment variables from .env file
from dotenv import load_dotenv
# Standard library
import os


# =========================
# Environment setup
# =========================
# Read values from .env file into environment
load_dotenv()

# Secret key used to sign and verify JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY")
# Algorithm used for JWT encoding/decoding (e.g. HS256)
ALGORITHM = os.getenv("ALGORITHM")


# =========================
# Access token validation
# =========================
async def check_access_token(access_token: str) -> str:
    """
    Validates JWT access token and extracts user ID.

    :param access_token: JWT access token string
    :return: user_id extracted from token payload
    :raises HTTPException: if token is expired or invalid
    """

    try:
        # Decode JWT token using secret key and algorithm
        payload = jwt.decode(
            access_token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )

        # Get user ID from token payload ("sub" = subject)
        user_id = payload.get("sub")


        return user_id
        

    # Token is valid but expired
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )
    
    # Token is invalid (wrong signature, wrong format, etc.)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )