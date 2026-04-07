from app.models.news_model import NewsModel
from app.utils.clean_html import clean_html
from app.utils.current_date import get_current_date
from typing import Optional
from pydantic import Field
from fastapi import HTTPException
from app.schemas.response.get_news_schema import NewsResponseSchema

# ===========================
# Create News Service
# ===========================
# This function creates a news item in the database.
# It validates the input data, cleans the content, and saves the news document.
# Returns a structured response schema.
# ===========================

async def create_news(
    title: str,
    content: str,
    authorId: str,
    authorEmail: str,
    status: str = "draft",
    coverImage: Optional[str] = None,
    tags: Optional[list[str]] = Field(default_factory=list),
) -> NewsResponseSchema:

    # ===========================
    # Tags processing
    # ===========================
    # Convert all tags to lowercase to keep them consistent
    tags = [tag.lower() for tag in tags] or []

    # ===========================
    # Clean content
    # ===========================
    # Sanitize HTML to prevent unsafe input
    clean_content = await clean_html(content)

    # ===========================
    # ====== Validate Data ======
    # ===========================

    # ---- Title Validation ----
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    if title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if len(title) > 100:
        raise HTTPException(status_code=400, detail="Title is too long")

    if len(title) < 3:
        raise HTTPException(status_code=400, detail="Title is too short")
    
    # ---- Unique Title Check ----
    if await NewsModel.find_one({"title": title}):
        raise HTTPException(status_code=400, detail="Title must be unique")

    # ---- Content Validation ----
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")
    
    if content.strip() == "":
        raise HTTPException(status_code=400, detail="Content cannot be empty") 

    if len(content) > 10000:
        raise HTTPException(status_code=400, detail="Content is too long")

    if len(content) < 10:
        raise HTTPException(status_code=400, detail="Content is too short")
    
    # ---- Author, Status and Cover Image Validation ----
    if not authorEmail:
        raise HTTPException(status_code=400, detail="Author: Firstname Lastname is required")

    if not authorId:
        raise HTTPException(status_code=400, detail="Author ID is required")

    if status not in ["draft", "published"]:
        raise HTTPException(status_code=400, detail="Status must be draft or published")

    if coverImage and not coverImage.startswith("http"):
        raise HTTPException(status_code=400, detail="Cover image must be a valid URL")

    # ===========================
    # ====== Create News ========
    # ===========================
    news_doc = NewsModel(
        title=title,
        content=clean_content,
        authorId=authorId,
        authorEmail=authorEmail,
        status=status,
        coverImage=coverImage,
        tags=tags,
        createdAt=get_current_date(),
        publishedAt=get_current_date() if status == "published" else None
    )

    # Save the document in MongoDB
    await news_doc.save()

    # ===========================
    # ====== Return Response =====
    # ===========================
    return NewsResponseSchema(
        id=str(news_doc.id),
        title=news_doc.title,
        content=news_doc.content,
        coverImage=news_doc.coverImage,
        status=news_doc.status,
        tags=news_doc.tags,
        createdAt=str(news_doc.createdAt),
        publishedAt=str(news_doc.publishedAt) if news_doc.publishedAt else None
    )