from fastapi import HTTPException

from bson import ObjectId
from ...models import WorkspaceProjectMemberModel

async def add_project_member(projectId: str, userId: str, role: str):
    
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project_member = WorkspaceProjectMemberModel(
        projectId=projectId,
        userId=userId,
        role=role
    )

    await project_member.save()

    return {"message": "Project member added successfully"}