from typing import Optional
from ...models import WorkspaceProjectModel
from ...schemas.response.workspace_project import WorkspaceProjectSchema


async def create_project(
    title: str,
    user_id: str,
    description: Optional[str] = None
):
    
    # If description not exist
    if description is None:
        description = ""

    # Create new project
    new_project = WorkspaceProjectModel(
        userId=user_id,
        title=title,
        description=description
    )

    # Save new document in MongoDb
    await new_project.save()

    return WorkspaceProjectSchema(
        id=str(new_project.id),              # ObjectId -> str
        userId=new_project.userId,
        title=new_project.title,
        description=new_project.description,
        createdAt=new_project.createdAt
    )
