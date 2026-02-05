from fastapi import (
    APIRouter, 
    Depends,
    Header,
    Response
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from sqlmodel import Session
from ..dependencies.data_base_connection import get_db
from ..services.modify_user.change_email_service import change_user_email
from ..services.modify_user.change_password_service import change_user_password
from ..services.modify_user.change_username_service import change_user_username
from ..services.tokens_management.refresh_tokens_service import check_access_token
from ..schemas.users.user_schema import UserSchema
from ..schemas.users.change_username_schema import ChangeUsernameSchema
from ..schemas.users.change_email_schema import ChangeEmailSchema
from ..schemas.users.change_password_schema import ChangePasswordSchema

# Router
router = APIRouter(
    prefix="/modifications", 
    tags=["User modification service"]
)

security = HTTPBearer()

# Change username
@router.put(
    "/username/", 
    response_model=UserSchema,
    summary="Change user username",
    description="Set user username in the database"
)
async def modify_username(
    data: ChangeUsernameSchema,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credentials.credentials

    # Access token check
    user_id = await check_access_token(access_token)
    
    user = await change_user_username(user_id, data.new_username, db)

    return user

# Change email
@router.put(
        "/email/", 
        response_model=UserSchema,
        summary="Change user email",
        description="Set user email in the database"
    )
async def modify_email(
    data: ChangeEmailSchema,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    access_token = credentials.credentials

    # Access token check
    user_id = await check_access_token(access_token)

    user = await change_user_email(user_id, data.new_email, db)

    return user

# Change password
@router.put(
        "/password/", 
        response_model=UserSchema,
        summary="Change user password",
        description="Set user password in the database"
    )
async def modify_password(
    data: ChangePasswordSchema,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    # Access token from Authorization: Bearer <token>
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    access_token = credentials.credentials

    # Access token check
    user_id = await check_access_token(access_token)

    user = await change_user_password(
        user_id=user_id, 
        old_password=data.old_password, 
        new_password=data.new_password, 
        db=db
    )

    return user