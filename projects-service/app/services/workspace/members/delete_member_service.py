from fastapi import HTTPException
from bson import ObjectId
from ...models import WorkspaceProjectMemberModel


async def delete_project_member(projectId: str, userId: str):
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_member = await WorkspaceProjectMemberModel.find_one({"projectId": projectId, "userId": userId})
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    await project_member.delete()

    return {"message": "Project member deleted successfully"}