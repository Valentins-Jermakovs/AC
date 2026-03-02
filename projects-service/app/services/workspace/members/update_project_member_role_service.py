from fastapi import HTTPException
from bson import ObjectId
from ...models import WorkspaceProjectMemberModel
from ...schemas.response.workspace_member import WorkspaceProjectMemberSchema

async def update_project_member_role(projectId: str, userId: str, role: str):
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    project_member = await WorkspaceProjectMemberModel.find_one({"projectId": projectId, "userId": userId})
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    project_member.role = role
    await project_member.save()

    return WorkspaceProjectMemberSchema(
        project_id=project_member.projectId,
        user_id=project_member.userId,
        role=project_member.role
    )
