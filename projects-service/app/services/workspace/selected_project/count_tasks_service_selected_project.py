# Imports
from bson import ObjectId
from app.models import WorkspaceTaskModel, WorkspaceProjectMemberModel

async def get_project_tasks_stats(
    project_id: str,
    user_id: str
) -> dict[str, int]:
    # Validation
    if not project_id or not ObjectId.is_valid(project_id):
        return {
            "totalTasks": 0,
            "todo": 0,
            "inProgress": 0,
            "done": 0
        }

    # Access check
    user = await WorkspaceProjectMemberModel.find_one({
        "projectId": project_id,
        "userId": user_id,
    })

    if not user:
        return {
            "totalTasks": 0,
            "todo": 0,
            "inProgress": 0,
            "done": 0
        }

    # Counts
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