# Imports
# Libraries
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
# Utils
from ..utils.check_admin_role import check_admin_role
# Dependencies
from .data_base_connection import get_db
security = HTTPBearer()


async def get_admin_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> int:
    
    token = credentials.credentials

    admin_user_id = await check_admin_role(token, db)

    if not admin_user_id:
        raise HTTPException(status_code=403, detail="Admin required")

    return admin_user_id