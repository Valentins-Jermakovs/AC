from datetime import date, timedelta
from app.models.activity_models import UserDailyActivity

# ================================================
# Get weekly statistics for a user
# ================================================
async def get_week_stats(user_id: str):
    today = date.today()                   # get today's date
    start = today - timedelta(days=6)     # calculate start date (7 days including today)

    # Fetch daily activity records for the last 7 days
    data = await UserDailyActivity.find(
        UserDailyActivity.user_id == user_id,
        UserDailyActivity.date >= start
    ).to_list()

    # Return aggregated statistics
    return {
        "active_days": len(data),                              # number of days with activity
        "total_time": sum(d.total_seconds for d in data),      # total time spent in seconds
        "total_visits": sum(d.visit_count for d in data),      # total number of visits
        "daily_breakdown": [                                   # detailed data per day
            {"date": d.date.isoformat(), 
             "seconds": d.total_seconds, 
             "visits": d.visit_count}
            for d in data
        ]
    }