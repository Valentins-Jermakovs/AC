# =========================
# IMPORTS
# =========================
from pydantic import BaseModel
from typing import Optional

# =========================
# NEWS RESPONSE SCHEMA
# =========================
class NewsResponseSchema(BaseModel):
    """
    Schema for a single news item response.
    
    Fields:
    - id: str - unique identifier of the news
    - title: str - news title
    - content: str - news content
    - coverImage: Optional[str] - cover image URL (optional)
    - status: str - news status ('draft' or 'published')
    - tags: list[str] - list of tags
    - createdAt: str - creation date
    - publishedAt: Optional[str] - published date (optional)
    """
    id: str
    title: str
    content: str
    coverImage: Optional[str] = None
    status: str
    tags: list[str]
    createdAt: str
    publishedAt: Optional[str] = None

    # JSON schema example for documentation
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "news_id",
                    "title": "News title",
                    "content": "News content",
                    "coverImage": "https://example.com/image.jpg",
                    "status": "draft",
                    "tags": ["tag1", "tag2"],
                    "createdAt": "2022-01-01",
                    "publishedAt": "2022-01-01"
                }
            ]
        }
    }


# =========================
# PAGINATION META SCHEMA
# =========================
class Meta(BaseModel):
    """
    Pagination metadata for paginated responses.
    
    Fields:
    - page: int - current page number
    - limit: int - items per page
    - total_pages: int - total number of pages
    - total_items: int - total number of items
    """
    page: int
    limit: int
    total_pages: int
    total_items: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "page": 1,
                    "limit": 10,
                    "total_pages": 2,
                    "total_items": 20
                }
            ]
        }
    }


# =========================
# NEWS RESPONSE PAGINATED SCHEMA
# =========================
class NewsResponseSchemaPaginated(BaseModel):
    """
    Schema for paginated list of news items.
    
    Fields:
    - data: list[NewsResponseSchema] - list of news items
    - meta: Meta - pagination metadata
    """
    data: list[NewsResponseSchema]
    meta: Meta

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
                            "id": "news_id",
                            "title": "News title",
                            "content": "News content",
                            "coverImage": "https://example.com/image.jpg",
                            "status": "draft",
                            "tags": ["tag1", "tag2"],
                            "createdAt": "2022-01-01",
                            "publishedAt": "2022-01-01"
                        }
                    ],
                    "meta": {
                        "page": 1,
                        "limit": 10,
                        "total_pages": 2,
                        "total_items": 20
                    }
                }
            ]
        }
    }