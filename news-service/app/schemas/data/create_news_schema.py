from pydantic import BaseModel, Field
from typing import Optional

class CreateNews(BaseModel):
    authorEmail: str
    title: str
    content: str
    coverImage: Optional[str]=None
    tags: Optional[list[str]] = Field(default_factory=list)
    status: str = "draft"

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