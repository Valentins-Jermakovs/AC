from datetime import date, timedelta
from app.models.activity_models import UserDailyActivity

async def get_week_stats(user_id: str):
    today = date.today()
    start = today - timedelta(days=6)  # 7 dienas, ieskaitot šodien

    data = await UserDailyActivity.find(
        UserDailyActivity.user_id == user_id,
        UserDailyActivity.date >= start
    ).to_list()

    return {
        "active_days": len(data),
        "total_time": sum(d.total_seconds for d in data),
        "total_visits": sum(d.visit_count for d in data),
        "daily_breakdown": [
            {"date": d.date.isoformat(), "seconds": d.total_seconds, "visits": d.visit_count}
            for d in data
        ]
    }