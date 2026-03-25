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

    project = await LastOpenedWorkspaceModel.find_one(LastOpenedWorkspaceModel.userId == userId)

    return project

# get selected project by uiser id
async def get_selected_project(user_id: str):
    project = await LastOpenedWorkspaceModel.find_one(LastOpenedWorkspaceModel.userId == user_id)

    return project

async def clear_selected_project_service(userId: str):
    # ===== Validation =====
    if not userId:
        raise HTTPException(status_code=400, detail="User ID required")

    # ===== Delete selected project =====
    await LastOpenedWorkspaceModel.find_one(
        LastOpenedWorkspaceModel.userId == userId
    ).delete()

    return {"detail": "Selected project cleared"}