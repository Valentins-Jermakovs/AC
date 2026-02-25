from fastapi import HTTPException
from typing import Optional
from ...models import WorkspaceProjectModel
from ...schemas.response.workspace_project import WorkspaceProjectSchema


async def get_project_by_title_or_description(
    title: Optional[str] = None,
    description: Optional[str] = None
):
    # If nothing provided
    if not title and not description:
        raise HTTPException(status_code=400, detail="Title or description required")

    query_conditions = []

    if title:
        query_conditions.append({
            "title": {"$regex": title, "$options": "i"}
        })

    if description:
        query_conditions.append({
            "description": {"$regex": description, "$options": "i"}
        })

    # If only one condition → no need for $or
    if len(query_conditions) == 1:
        project = await WorkspaceProjectModel.find_one(query_conditions[0])
    else:
        project = await WorkspaceProjectModel.find_one({
            "$or": query_conditions
        })

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return WorkspaceProjectSchema(
        id=str(project.id),
        userId=project.userId,
        title=project.title,
        description=project.description,
        createdAt=project.createdAt,
    )