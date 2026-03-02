from fastapi import HTTPException
from bson import ObjectId
from ...models import WorkspaceProjectModel

async def delete_project(project_id: str):
    
    # Raise if project_id is not valid
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Try to find project
    project = await WorkspaceProjectModel.find_one({"_id": ObjectId(project_id)})

    # Raise if project not found
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete project
    await project.delete()

    return {"message": f"Project '{project.title}' deleted successfully"}