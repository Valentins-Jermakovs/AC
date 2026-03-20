# Imports
import datetime
# Models
from app.models import PrivateTaskModel

'''
    Get all private tasks from the database (count)

    Steps:
    1. Get all private tasks from the database
    2. Return paginated tasks
'''

# =======================================
# Get all private tasks from the database
# =======================================
async def get_all_private_tasks_counted(
    user_id: str
) -> int:
    
    tasks_count = await PrivateTaskModel.find({
        "userId": user_id
    }).count()
    return tasks_count

# =======================================================
# Get all private completed tasks from the database
# =======================================================
async def get_all_private_completed_tasks_counted(
    user_id: str
) -> int:
    
    tasks_count = await PrivateTaskModel.find({
        "userId": user_id, 
        "completed": True
    }).count()
    return tasks_count

# =======================================================
# Get all private tasks in this month from the database
# =======================================================
async def get_all_private_tasks_by_current_month(
    user_id: str
) -> int:
    
    month = datetime.datetime.now().month

    tasks_count = await PrivateTaskModel.find({
        "userId": user_id, 
        "$expr": { "$eq": [{ "$month": "$dueDate" }, month] }
    }).count()
    return tasks_count

# ===============================================================
# Get all private completed tasks in this month from the database
# ===============================================================
async def get_all_private_completed_tasks_by_current_month(
    user_id: str
) -> int:
    
    month = datetime.datetime.now().month
    
    tasks_count = await PrivateTaskModel.find({
        "userId": user_id, 
        "completed": True, 
        "$expr": { "$eq": [{ "$month": "$dueDate" }, month] }
    }).count()
    return tasks_count
