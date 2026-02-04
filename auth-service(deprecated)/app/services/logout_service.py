# Imports
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.models import Token


"""
===== Logout Service =====
Function: logout
----------------
Logs out a user by invalidating their refresh token.

Parameters:
- db (Session): SQLModel database session for querying and modifying tokens.
- refresh_token (str): The refresh token string provided by the client for logout.

Process:
1. Looks up the provided refresh token in the database.
2. Raises HTTP 401 if the token does not exist (invalid token).
3. Deletes the token from the database to log the user out.
4. Commits the transaction to persist the changes.
5. Returns a confirmation message indicating successful logout.

Raises:
- HTTPException with status code 401 if the refresh token is invalid.
"""


# Logout user
async def logout(db: Session, refresh_token: str):

    # Refresh token check
    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    # Delete refresh token
    db.delete(token)
    db.commit()

    # Confirmation
    return {"message": "Logout successful"}