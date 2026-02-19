from datetime import datetime
from ..models.private_task import PrivateTask

from fastapi import APIRouter

router = APIRouter()

@router.post("/tasks/test")
async def create_test_task():
    task = PrivateTask(
        userId="1234",
        title="Test Task",
        description="This is a test",
        dueDate=datetime(2026, 2, 28)
    )
    await task.insert()
    return {"id": str(task.id), "message": "Task created"}
