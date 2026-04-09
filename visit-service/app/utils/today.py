from datetime import date
from app.models.activity_models import UserDailyActivity

# ================================================
# Get today's activity for a user, create if missing
# ================================================
async def get_today(user_id: str) -> UserDailyActivity:
    today = date.today()  # get today's date

    # Try to find existing activity for today
    activity = await UserDailyActivity.find_one(
        UserDailyActivity.user_id == user_id,
        UserDailyActivity.date == today
    )

    # If no activity exists, create a new record
    if not activity:
        from datetime import datetime
        now = datetime.now()  # current timestamp
        activity = UserDailyActivity(
            user_id=user_id,
            date=today,
            first_visit=now,
            last_visit=now,
            sessions=[]
        )
        await activity.insert()  # save new activity to database

    return activity  # return today's activity