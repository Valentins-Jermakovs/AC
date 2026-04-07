from pydantic import BaseModel
from typing import Optional

class NewsResponseSchema(BaseModel):
    id: str
    title: str
    content: str
    coverImage: Optional[str]
    status: str
    tags: list[str]
    createdAt: str
    publishedAt: Optional[str]

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

class Meta(BaseModel):
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

class GetNewsResponseSchema(BaseModel):
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