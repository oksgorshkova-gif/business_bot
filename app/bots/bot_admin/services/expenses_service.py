from datetime import datetime, date
from app.config import months
from app.bots.bot_admin.db.connection import get_connection

def register_expense(category, amount, spending_date=None, comment=None):

    if spending_date is None:
        spending_date = date.today()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO expenses (amount, category, date, comment)
            VALUES (%s, %s, %s, %s)
            """,
            (amount, category, spending_date, comment)
        )
        conn.commit()
        print(f'Добавлена трата {amount} руб. в категорию "{category}".')
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при записи траты в базу данных в register_expense:\n{e}")
        raise e
    finally:
        cursor.close()
        conn.close()
    
def register_mortgage_payment():
    category = "mortgage"
    amount = 24875
    day = date.today().replace(day=4)  
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO expenses (category, amount, date)
            VALUES (%s, %s, %s)
            """,
            (category, amount, day)
        )
        conn.commit()
        print(f"За ипотеку внесено {amount} за {months.get(day.month, 'месяц')}")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при записи платежа по ипотеке в базу данных:\n{e}")
        raise e
    finally:
        cursor.close()
        conn.close()
    
    category = "charges"
    amount = 2198
    day = date.today().replace(day=4) 
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO expenses (amount, category, date)
            VALUES (%s, %s, %s)
            """,
            (amount, category, day)
        )
        conn.commit()
        print(f"За КУ внесено {amount} за {months.get(day.month, 'месяц')}")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при записи траты на КУ в базу данных:\n{e}")
        raise e 
    finally:
        cursor.close()
        conn.close()
    
def parse_expense_raw_text(text):
    try:
        text_parts = text.split("\n")
        amount = int(text_parts[0].strip())
        comment = text_parts[1].strip() if len(text_parts) > 1 else ""
        date_str = text_parts[2].strip() if len(text_parts) > 2 else ""
        dt = datetime.strptime(date_str, "%d.%m.%y") if date_str else date.today()

        if len(text_parts) == 3:
            category = "extra"
        elif len(text_parts) == 4:
            category = "extra-mortgage"
        return [amount, comment, dt, category]
    except Exception as e:
        print(f"Ошибка при парсинге данных:\n{e}")
        raise e 
