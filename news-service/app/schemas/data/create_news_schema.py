# =========================
# IMPORTS
# =========================
from pydantic import BaseModel, Field
from typing import Optional

# =========================
# CREATE NEWS SCHEMA
# =========================
class CreateNews(BaseModel):
    """
    Schema for creating a news item.

    Fields:
    - authorEmail: str - email of the news author
    - title: str - title of the news
    - content: str - content of the news
    - coverImage: Optional[str] - URL of the cover image (optional)
    - tags: Optional[list[str]] - list of tags (optional, default empty list)
    - status: str - news status, can be 'draft' or 'published' (default 'draft')
    """
    authorEmail: str
    title: str
    content: str
    coverImage: Optional[str] = None
    tags: Optional[list[str]] = Field(default_factory=list)
    status: str = "draft"

    # =========================
    # JSON Schema Examples
    # =========================
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "authorEmail": "2V2E3@example.com",
                    "title": "News title",
                    "content": "News content",
                    "coverImage": "https://example.com/image.jpg",
                    "tags": ["tag1", "tag2"],
                    "status": "draft"
                }
            ]
        }
    }