import psycopg2
from app import config

def get_connection():
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
    )
def moving_from_txt_to_db(id, name):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO clients (id, name) VALUES (%s, %s)",
                (id, name)
            )
        conn.commit()
        print(f"Добавили {id} {name}")
        return id, name
    except Exception as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        raise

def refresh_clients_list():
    with open(config.LOG_FILE, 'r', encoding='utf-8') as f:
        for l in f:
            res = l.split(' | ')[1].split()
            if len(res) < 3:
                continue
            id = res[1]
            name = res[3]
            moving_from_txt_to_db(id, name)




        

        
