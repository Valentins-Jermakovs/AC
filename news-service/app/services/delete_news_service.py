from fastapi import HTTPException
from app.models.news_model import NewsModel
from bson import ObjectId

# ===========================
# Delete News Service
# ===========================
# This function deletes a news item from the database by its ID.
# It validates the ID, checks if the news exists, and deletes it.
# Returns a simple success message.
# ===========================

async def delete_news(
    newsId: str
) -> dict:

    # ===========================
    # ===== Validate ID ========
    # ===========================
    # Check if the provided ID is a valid MongoDB ObjectId
    if not ObjectId.is_valid(newsId):
        raise HTTPException(status_code=400, detail="Invalid news ID")

    # ===========================
    # ===== Find News ==========
    # ===========================
    # Try to find the news document in the database
    news_doc = await NewsModel.find_one({"_id": ObjectId(newsId)})

    # Raise 404 error if news not found
    if not news_doc:
        raise HTTPException(status_code=404, detail="News not found")
    
    # ===========================
    # ===== Delete News ========
    # ===========================
    # Remove the news document from the database
    await news_doc.delete()

    # ===========================
    # ===== Return Response =====
    # ===========================
    # Return a simple confirmation message
    return {"message": "News deleted successfully"}