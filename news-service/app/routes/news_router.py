# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Schemas
from app.schemas.data.create_news_schema import CreateNews
from app.schemas.data.update_news_schema import UpdateNewsSchema
from app.schemas.response.get_news_schema import NewsResponseSchema, NewsResponseSchemaPaginated

# Services
from app.services.create_news_service import create_news
from app.services.update_news_service import update_news
from app.services.delete_news_service import delete_news
from app.services.get_news_service import get_news_paginated

# Utilities
from app.utils.check_access_token import check_access_token

# =========================
# ROUTER SETUP
# =========================
router = APIRouter(
    prefix="/news",
    tags=["News management service"]
)

# Authentication dependency using HTTP Bearer token
security = HTTPBearer()


# =========================
# CREATE NEWS ROUTE
# =========================
@router.post(
    "/create", 
    response_model=NewsResponseSchema
)
async def create_news_route(
    data: CreateNews,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new news item.

    - Requires authentication
    - Validates user via access token
    - Uses `create_news` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await create_news(
        authorEmail=data.authorEmail,
        authorId=user_id,
        content=data.content,
        coverImage=data.coverImage,
        status=data.status,
        tags=data.tags,
        title=data.title
    )

# =========================
# GET NEWS ROUTE (PAGINATED)
# =========================
@router.get(
    "/get", 
    response_model=NewsResponseSchemaPaginated
)
async def get_news_route(
    limit: int = 10,
    page: int = 1,
    query: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get paginated news list.

    - Supports optional search query
    - Requires authentication
    - Uses `get_news_paginated` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_news_paginated(
        limit=limit,
        page=page,
        query=query
    )


# =========================
# UPDATE NEWS ROUTE
# =========================
@router.put(
    "/update", 
    response_model=NewsResponseSchema
)
async def update_news_route(
    data: UpdateNewsSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update an existing news item by ID.

    - Requires authentication
    - Validates user via access token
    - Uses `update_news` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await update_news(
        content=data.content,
        coverImage=data.coverImage,
        status=data.status,
        tags=data.tags,
        title=data.title,
        newsId=data.id
    )


# =========================
# DELETE NEWS ROUTE
# =========================
@router.delete("/delete/{id}")
async def delete_news_route(
    newsId: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete a news item by ID.

    - Requires authentication
    - Uses `delete_news` service
    """
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await delete_news(
        newsId=newsId
    )
