# =========================
# IMPORTS
# =========================
from pydantic import BaseModel
from typing import Optional

# =========================
# UPDATE NEWS SCHEMA
# =========================
class UpdateNewsSchema(BaseModel):
    """
    Schema for updating a news item.

    Fields:
    - id: str - unique identifier of the news to update
    - title: Optional[str] - new title (optional)
    - content: Optional[str] - new content (optional)
    - coverImage: Optional[str] - new cover image URL (optional)
    - tags: Optional[list[str]] - new list of tags (optional)
    - status: Optional[str] - new status, can be 'draft' or 'published' (optional)
    """
    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    coverImage: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None

    # =========================
    # JSON Schema Examples
    # =========================
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "news_id",
                    "title": "Updated title",
                    "content": "Updated content",
                    "coverImage": "https://example.com/image.jpg",
                    "tags": ["tag1", "tag2"],
                    "status": "draft"
                }
            ]
        }
    }