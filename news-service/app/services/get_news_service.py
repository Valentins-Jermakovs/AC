from fastapi import HTTPException
from typing import Optional
from app.models.news_model import NewsModel
from app.schemas.response.get_news_schema import (
    NewsResponseSchema,
    Meta,
    NewsResponseSchemaPaginated
)
import re
import math

# ===========================
# Get News Paginated Service
# ===========================
# This function returns paginated news data.
# Supports:
# - pagination (page + limit)
# - search query filtering
# - sorting by creation date (newest first)
# Returns structured paginated response.
# ===========================

async def get_news_paginated(
    limit: int = 10,
    page: int = 1,
    query: Optional[str] = None
) -> NewsResponseSchemaPaginated:

    # ===========================
    # ===== Pagination Fix ======
    # ===========================
    # Prevent invalid pagination values
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    # ===========================
    # ===== Build Filters =======
    # ===========================
    # Default filter (no filtering)
    filters = {}

    # If search query exists, build regex search
    # This allows partial and case-insensitive search
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

    # ===========================
    # ===== Count Items =========
    # ===========================
    # Count total matching documents
    total_items = await NewsModel.find(filters).count()

    # Calculate total pages (minimum = 1)
    total_pages = max(math.ceil(total_items / limit), 1)

    # Calculate how many items to skip
    skip = (page - 1) * limit

    # ===========================
    # ===== Fetch Data ==========
    # ===========================
    # Get filtered news sorted by newest first
    news_docs = await NewsModel.find(filters)\
        .sort("-createdAt")\
        .skip(skip)\
        .limit(limit)\
        .to_list()

    # ===========================
    # ===== Map To Schema =======
    # ===========================
    # Convert database documents into response schema objects
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

    # ===========================
    # ===== Build Meta ==========
    # ===========================
    # Create pagination metadata
    meta = Meta(
        page=page,
        limit=limit,
        total_pages=total_pages,
        total_items=total_items,
    )

    # ===========================
    # ===== Page Validation =====
    # ===========================
    # If requested page does not exist
    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    # ===========================
    # ===== Return Response =====
    # ===========================
    return NewsResponseSchemaPaginated(
        data=data,
        meta=meta
    )