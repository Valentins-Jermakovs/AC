from ...models import WorkspaceProjectModel
from ...schemas.response.workspace_project import WorkspaceProjectSchema

async def get_all_projects(user_id: str):

    projects = await WorkspaceProjectModel.find({"userId": user_id}).to_list()

    # Get all projects from the database
    items = [
        WorkspaceProjectSchema(
            id=str(project.id),
            userId=project.userId,
            title=project.title,
            description=project.description,
            createdAt=project.createdAt,
        )
        for project in projects
    ]

    return {
        "items": items
    }