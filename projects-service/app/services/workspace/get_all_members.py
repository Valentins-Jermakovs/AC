from fastapi import HTTPException
from bson import ObjectId
from ...models import WorkspaceProjectMemberModel
from ...schemas.response.workspace_member import WorkspaceProjectMemberSchema


async def get_all_project_members(projectId: str):

    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    members = await WorkspaceProjectMemberModel.find(
        WorkspaceProjectMemberModel.projectId == projectId
    ).to_list()

    if not members:
        raise HTTPException(status_code=404, detail="Members not found")

    return {
        "members": [
            WorkspaceProjectMemberSchema(
                project_id=member.projectId,
                user_id=member.userId,
                role=member.role
            )
            for member in members
        ]
    }