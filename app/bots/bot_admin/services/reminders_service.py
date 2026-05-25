from datetime import timedelta

def format_timedelta(td: timedelta) -> str:
    """Безопасное форматирование timedelta в ЧЧ:ММ"""
    total_seconds = int(td.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, _ = divmod(rem, 60) 
    return f"{hours}:{minutes:02}"

def get_today_bookings():
    ...

def send_reminders(bot):
    ...