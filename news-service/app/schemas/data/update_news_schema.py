from pydantic import BaseModel
from typing import Optional

class UpdateNewsSchema(BaseModel):
    id: str
    title: Optional[str]
    content: Optional[str]
    coverImage: Optional[str]
    tags: Optional[list[str]]
    status: Optional[str]

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