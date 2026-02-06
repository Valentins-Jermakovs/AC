# =========================
# Logout service
# =========================
from sqlmodel import Session, select
from fastapi import HTTPException
# Database model
from ...models import Token


# =========================
# Logout user
# =========================
async def logout(db: Session, refresh_token: str):
    """
    Logs out a user by invalidating their refresh token.

    Steps:
    1. Look up the provided refresh token in the database
    2. Raise 401 if token does not exist (invalid token)
    3. Delete the token to log out the user
    4. Commit changes to persist deletion
    5. Return confirmation message

    :param db: SQLModel database session
    :param refresh_token: refresh token string from client
    :return: dict with confirmation message
    :raises HTTPException: 401 if token is invalid
    """

    # Find the refresh token in database
    token = db.exec(
        select(Token).where(Token.refresh_token == refresh_token)
    ).first()

    # Token not found → unauthorized
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    # Delete token to log user out
    db.delete(token)
    db.commit()

    # Return confirmation
    return {"message": "Logout successful"}