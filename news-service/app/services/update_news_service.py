from app.models.news_model import NewsModel, StatusEnum
from app.utils.clean_html import clean_html
from app.utils.current_date import get_current_date
from fastapi import HTTPException
from typing import Optional
from app.schemas.response.get_news_schema import NewsResponseSchema
from bson import ObjectId

# ===========================
# Update News Service
# ===========================
# This function updates an existing news item.
# Only provided fields will be updated.
#
# Supports updating:
# - title
# - content
# - cover image
# - tags
# - status
#
# Returns updated news as response schema.
# ===========================

async def update_news(
    newsId: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    coverImage: Optional[str] = None,
    tags: Optional[list[str]] = None,
    status: Optional[str] = None
) -> NewsResponseSchema:

    # ===========================
    # ===== Find News ===========
    # ===========================
    # Find news document by ID
    news_doc = await NewsModel.find_one({"_id": ObjectId(newsId)})

    # If news does not exist → return 404
    if not news_doc:
        raise HTTPException(status_code=404, detail="News not found")
    
    # ===========================
    # ===== Update Fields =======
    # ===========================
    # Update only fields that were provided

    # ---- Title Update ----
    if title:
        title = title.strip()

        # Validate title length
        if len(title) < 3:
            raise HTTPException(status_code=400, detail="Title is too short")

        if len(title) > 100:
            raise HTTPException(status_code=400, detail="Title is too long")

        # Check title uniqueness (exclude current document)
        existing = await NewsModel.find_one({
            "title": title,
            "_id": {"$ne": ObjectId(newsId)}
        })

        if existing:
            raise HTTPException(status_code=400, detail="Title must be unique")

        # Apply update
        news_doc.title = title
    
    # ---- Content Update ----
    if content:
        content = content.strip()

        # Validate content length
        if len(content) < 10:
            raise HTTPException(status_code=400, detail="Content is too short")

        if len(content) > 10000:
            raise HTTPException(status_code=400, detail="Content is too long")

        # Clean HTML before saving
        news_doc.content = await clean_html(content)

    # ---- Cover Image Update ----
    if coverImage:

        # Simple URL validation
        if not coverImage.startswith("http"):
            raise HTTPException(status_code=400, detail="Cover image must be a valid URL")

        news_doc.coverImage = coverImage

    # ---- Tags Update ----
    if tags:
        # Normalize tags to lowercase
        news_doc.tags = [tag.lower() for tag in tags]

    # ---- Status Update ----
    if status:

        # Validate allowed values
        if status not in ['draft', 'published']:
            raise HTTPException(
                status_code=400,
                detail="Status must be 'draft' or 'published'"
            )

        # Update status enum
        news_doc.status = StatusEnum(status)

        # Handle publish date logic
        if status == "published" and not news_doc.publishedAt:
            news_doc.publishedAt = get_current_date()

        elif status == "draft":
            news_doc.publishedAt = None
    
    # ===========================
    # ===== Save Changes ========
    # ===========================
    # Save updated document
    await news_doc.save()

    # ===========================
    # ===== Return Response =====
    # ===========================
    # Return updated news data
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