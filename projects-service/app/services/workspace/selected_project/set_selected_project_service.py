# Imports
from fastapi import HTTPException
from bson import ObjectId
# Models
from app.models import LastOpenedWorkspaceModel

async def set_selected_project_service(
    userId: str, 
    workspaceId: str,
    workspaceTitle: str
):

    # ===== Validation =====
    if not userId:
        raise HTTPException(status_code=400, detail="User ID required")

    if not workspaceId:
        raise HTTPException(status_code=400, detail="Workspace ID required")

    if not ObjectId.is_valid(workspaceId):
        raise HTTPException(status_code=400, detail="Invalid workspace ID")
    

    # ===== Create or update selected project =====
    await LastOpenedWorkspaceModel.find_one(
        LastOpenedWorkspaceModel.userId == userId
    ).upsert(
        {
            "$set": {
                "workspaceId": workspaceId,
                "workspaceTitle": workspaceTitle
            }
        },
        on_insert=LastOpenedWorkspaceModel(
            userId=userId,
            workspaceId=workspaceId,
            workspaceTitle=workspaceTitle
        )
    )

    return workspaceTitle