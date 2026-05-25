from app.config import PASSWORD
from app.bots.bot_admin.db.connection import get_connection as connection

def check_password(user_id, password):
    if password == PASSWORD: 
        print("Password correct") 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(
                """
                INSERT INTO authorized_users (id)
                VALUES (%s)
                ON CONFLICT (id) DO NOTHING
                """,
                (user_id,)
            )
        conn.commit()
        return True
    print("Password incorrect") 
    return False


def is_authorized(user_id):
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM authorized_users WHERE id = %s",
            (user_id,)
        )
        result = cursor.fetchone()
        print("Пускаю пользователя", *result)
        return result is not None
    except Exception as e:
        print(e) 
        return False
    finally:
        cursor.close()
        conn.close()
