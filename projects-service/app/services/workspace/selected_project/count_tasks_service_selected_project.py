# Imports
from fastapi import HTTPException
from bson import ObjectId

# Models
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel


async def get_project_tasks_stats(
    project_id: str,
    user_id: str
):

    # ===== Validation =====
    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required")

    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    # ===== Access check =====
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        raise HTTPException(
            status_code=403,
            detail="You are not member of this project"
        )

    # ===== Counts =====
    todo = await WorkspaceTaskModel.find({
        "projectId": project_id,
        "status": "todo"
    }).count()

    in_progress = await WorkspaceTaskModel.find({
        "projectId": project_id,
        "status": "in_progress"
    }).count()

    done = await WorkspaceTaskModel.find({
        "projectId": project_id,
        "status": "done"
    }).count()

    total = todo + in_progress + done

    return {
        "totalTasks": total,
        "todo": todo,
        "inProgress": in_progress,
        "done": done
    }