from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.data.create_news_schema import CreateNews
from app.schemas.data.update_news_schema import UpdateNewsSchema
from app.services.create_news_service import create_news
from app.services.update_news_service import update_news
from app.services.delete_news_service import delete_news
from app.services.get_news_service import get_news_paginated
from app.schemas.response.get_news_schema import NewsResponseSchema
from app.schemas.response.get_news_schema import NewsResponseSchemaPaginated
# Utils
from app.utils.check_access_token import check_access_token

router = APIRouter(
    prefix="/news",
    tags=["News management service"]
)

# Authentication
security = HTTPBearer()


@router.post("/create", response_model=NewsResponseSchema)
async def create_news_route(
    data: CreateNews, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    
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


@router.put("/update", response_model=NewsResponseSchema)
async def update_news_route(
    data: UpdateNewsSchema, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    
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


@router.delete("/delete")
async def delete_news_route(
    newsId: str, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await delete_news(
        newsId=newsId
    )


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
    
    access_token = credentials.credentials
    user_id = await check_access_token(access_token)

    return await get_news_paginated(
        limit=limit,
        page=page,
        query=query
    )