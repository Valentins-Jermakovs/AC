from app.models.news_model import NewsModel, StatusEnum
from app.utils.clean_html import clean_html
from app.utils.current_date import get_current_date
from fastapi import HTTPException
from typing import Optional
from app.schemas.response.get_news_schema import NewsResponseSchema
from bson import ObjectId

async def update_news(
    newsId: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    coverImage: Optional[str] = None,
    tags: Optional[list[str]] = None,
    status: Optional[str] = None
) -> NewsResponseSchema:
    
    news_doc = await NewsModel.find_one({"_id": ObjectId(newsId)})

    if not news_doc:
        raise HTTPException(status_code=404, detail="News not found")
    
    # Update fields if provided
    if title:
        title = title.strip()
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")
        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")
        # check title unique (skip self)
        existing = await NewsModel.find_one({
            "title": title, 
            "_id": {"$ne": ObjectId(newsId)}
        })
        if existing:
            raise HTTPException(status_code=400, detail="Title must be unique")
        news_doc.title = title
    
    if content:
        content = content.strip()
        if len(content) < 10:
            raise HTTPException(status_code=400, detail="Content is too short")
        if len(content) > 10000:
            raise HTTPException(status_code=400, detail="Content is too long")
        news_doc.content = await clean_html(content)

    if coverImage:
        if not coverImage.startswith("http"):
            raise HTTPException(status_code=400, detail="Cover image must be a valid URL")
        news_doc.coverImage = coverImage

    if tags:
        news_doc.tags = [tag.lower() for tag in tags]

    if status:
        if status not in ['draft', 'published']:
            raise HTTPException(status_code=400, detail="Status must be 'draft' or 'published'")
        news_doc.status = StatusEnum(status)
        if status == "published" and not news_doc.publishedAt:
            news_doc.publishedAt = get_current_date()
        elif status == "draft":
            news_doc.publishedAt = None
    
    # Save changes
    await news_doc.save()

    # Return updated schema
    return NewsResponseSchema(
        id=str(news_doc.id),
        title=news_doc.title,
        content=news_doc.content,
        coverImage=news_doc.coverImage,
        status=news_doc.status,
        tags=news_doc.tags,
        createdAt=str(news_doc.createdAt),
        publishedAt=str(news_doc.publishedAt)
    )