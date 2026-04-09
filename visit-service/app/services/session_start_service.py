from datetime import datetime
from app.models.activity_models import Session
from app.utils.today import get_today

async def start_session(user_id: str):
    now = datetime.now()
    activity = await get_today(user_id)

    # Pievieno jaunu session tikai ja nav aktīva
    if not activity.sessions or activity.sessions[-1].end is not None:
        activity.sessions.append(Session(start=now))
        await activity.save()