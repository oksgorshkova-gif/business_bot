from datetime import datetime
from functools import wraps


def log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        print(f"[START] {func.__name__}")  

        try:
            result = await func(*args, **kwargs)

            print(f"[END] {func.__name__}") 

            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()} | {func.__name__} успешно завершена\n")
            
            return result

        except Exception as e:
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()} | ERROR {func.__name__}: {e}\n")

            print(f"[ERROR] {func.__name__}: {e}") 
            raise

    return wrapper


