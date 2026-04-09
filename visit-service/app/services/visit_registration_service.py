from datetime import datetime, date
from app.models.activity_models import UserDailyActivity, Session
from app.utils.today import get_today

async def register_visit(user_id:str):

    now = datetime.now()
    activity = await get_today(user_id)

    if not activity.sessions or activity.sessions[-1].end is not None:
        activity.sessions.append(Session(start=now))

    activity.last_visit = now
    activity.visit_count += 1
    await activity.save()