from datetime import date
from app.models.activity_models import UserDailyActivity

async def get_today(user_id: str) -> UserDailyActivity:
    today = date.today()
    activity = await UserDailyActivity.find_one(
        UserDailyActivity.user_id == user_id,
        UserDailyActivity.date == today
    )
    if not activity:
        from datetime import datetime
        now = datetime.now()
        activity = UserDailyActivity(
            user_id=user_id,
            date=today,
            first_visit=now,
            last_visit=now,
            sessions=[]
        )
        await activity.insert()
    return activity