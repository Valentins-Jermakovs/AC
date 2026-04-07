from fastapi import HTTPException
from bson import ObjectId
from typing import Optional
from app.models.news_model import NewsModel
from app.schemas.response.get_news_schema import (
    NewsResponseSchema,
    Meta,
    NewsResponseSchemaPaginated
)
import re
import math

async def get_news_paginated(
    limit: int = 10,
    page: int = 1,
    query: Optional[str] = None
) -> NewsResponseSchemaPaginated:
    
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    filters = {}

    if query:
        q = re.compile(re.escape(query), re.IGNORECASE)
        filters = {
            "$or": [
                {"title": q},
                {"content": q},
                {"status": q},
                {"tags": q},
                {"authorEmail": q},
            ]
        }

    total_items = await NewsModel.find(filters).count()
    total_pages = max(math.ceil(total_items / limit), 1)

    skip = (page - 1) * limit

    # fetch data sorted by createdAt descending
    news_docs = await NewsModel.find(filters).sort("-createdAt").skip(skip).limit(limit).to_list()

    # map to schema
    data = [
        NewsResponseSchema(
            id=str(news.id),
            title=news.title,
            content=news.content,
            coverImage=news.coverImage,
            status=news.status,
            tags=news.tags,
            createdAt=str(news.createdAt),
            publishedAt=str(news.publishedAt) if news.publishedAt else None,
        )
        for news in news_docs
    ]

    meta = Meta(
        page=page,
        limit=limit,
        total_pages=total_pages,
        total_items=total_items,
    )

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    return NewsResponseSchemaPaginated(
        data=data, 
        meta=meta
    )
