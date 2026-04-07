from fastapi import HTTPException
from app.models.news_model import NewsModel
from bson import ObjectId

async def delete_news(
    newsId: str
) -> dict:
    
    if not ObjectId.is_valid(newsId):
        raise HTTPException(status_code=400, detail="Invalid news ID")

    news_doc = await NewsModel.find_one({"_id": ObjectId(newsId)})

    if not news_doc:
        raise HTTPException(status_code=404, detail="News not found")
    
    await news_doc.delete()

    return {"message": "News deleted successfully"}