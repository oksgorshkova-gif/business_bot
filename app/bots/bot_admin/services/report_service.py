import datetime
from datetime import datetime, timedelta
from app.bots.bot_admin.db.connection import get_connection


def get_profit(period):
    date_start, date_end = period
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
                  """
                    SELECT SUM(price) FROM bookings
                    WHERE start_time >= %s AND end_time <= %s
                    """,
                    (date_start, date_end)
                )   
        total_income = cursor.fetchone()[0] or 0
        return total_income
    
    except Exception as e:
        print(f"Ошибка с базой данных:\n{e}")
        raise e
    finally:
        cursor.close()
        conn.close()
     
def get_expences(period):
    date_start, date_end = period
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
                  """
                    SELECT SUM(amount) FROM expenses
                    WHERE date >= %s AND date <= %s
                    """,
                    (date_start, date_end)
                )   
        total_expense = cursor.fetchone()[0] or 0
        return total_expense
    
    except Exception as e:
        print(f"Ошибка с базой данных:\n{e}")
        raise e
    finally:
        cursor.close()
        conn.close()
   
def get_period(period):
    now = datetime.now()

    if period == "Текущий месяц":
        offset = 0
    elif period == "Следующий месяц":
        offset = 1
    else:
        pass

    # сдвигаем месяц
    month = (now.month - 1 + offset) % 12 + 1
    year = now.year + ((now.month - 1 + offset) // 12)

    start = datetime(year, month, 1)

    # следующий месяц
    next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    end = next_month - timedelta(seconds=1)

    return start, end

def get_range(report_range):
    if "-" in report_range:
        date_start_str, date_end_str = [d.strip() for d in report_range.split("-")]
        date_start = datetime.strptime(date_start_str, "%d.%m.%y")
        date_end = datetime.strptime(date_end_str, "%d.%m.%y")

        date_start = date_start.replace(hour=0, minute=0, second=0)
        date_end = date_end.replace(hour=23, minute=59, second=59)

        if date_end < date_start:
            raise ValueError("Дата конца должна быть позже даты начала.")
    else:
        raise ValueError("Неверный формат. Введите период в формате ДД.ММ.ГГ-ДД.ММ.ГГ")
    return date_start, date_end
    




