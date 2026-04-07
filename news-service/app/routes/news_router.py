from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.data.create_news_schema import CreateNews
from app.services.create_news_service import create_news
# Utils
from app.utils.check_access_token import check_access_token

router = APIRouter(
    prefix="/news",
    tags=["News management service"]
)

# Authentication
security = HTTPBearer()


@router.post("/create")
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
