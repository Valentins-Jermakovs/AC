from pydantic import BaseModel
class MessageResponse(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Budget deleted successfully"
                }
            ]
        }
    }