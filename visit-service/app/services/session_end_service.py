from datetime import datetime
from app.utils.today import get_today

async def end_session(user_id: str):
    now = datetime.now()
    activity = await get_today(user_id)

    if not activity.sessions or activity.sessions[-1].end is not None:
        # nav aktīvas sesijas
        return

    session = activity.sessions[-1]
    session.close(now)
    activity.total_seconds += session.duration
    await activity.save()