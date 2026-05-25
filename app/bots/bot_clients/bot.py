import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton

from googleapiclient.discovery import build
from google.oauth2 import service_account

import psycopg2

from app import config
logging.basicConfig(level=logging.DEBUG)

# =====================
# НАСТРОЙКИ
# =====================

TOKEN = config.CLIENT_BOT_TOKEN
CALENDAR_ID = config.CALENDAR_ID

SCOPES = config.SCOPES
SERVICE_ACCOUNT_FILE = config.GOOGLE_SERVICE_ACCOUNT_FILE
SERVICE_ACCOUNT_JSON = config.GOOGLE_SERVICE_ACCOUNT_JSON
BASE_DIR = Path(__file__).resolve().parent

# =====================
# GOOGLE CALENDAR
# =====================
if SERVICE_ACCOUNT_JSON:
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_JSON),
        scopes=SCOPES,
    )
elif SERVICE_ACCOUNT_FILE:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
else:
    raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SERVICE_ACCOUNT_FILE is required")

service = build('calendar', 'v3', credentials=credentials)

# =====================
# Bot
# =====================
if not TOKEN:
    raise RuntimeError("CLIENT_BOT_TOKEN is required to run the client bot")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# хранилище (временно)
user_data = {}

# =====================
# KEYBOARDS
# =====================
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Проверить дату")],
        [KeyboardButton(text="🛎️ Забронировать")],
        [KeyboardButton(text="💳 Узнать стоимость")],
        [KeyboardButton(text="↩️ Правила отмены бронирования")],
        [KeyboardButton(text="📟 Связаться с нами")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)   

# =====================
# ФУНКЦИИ
# =====================

def get_connection():
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
    )


def write_log(line: str):
    log_path = Path(config.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)

def get_user_name(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM clients WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        name = cursor.fetchone()
        return name[0]
    except Exception as e:
        print(f"Error occurred in get_user_name: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_busy_intervals(date):
    start_of_day = datetime.strptime(date, "%d.%m.%y")
    end_of_day = start_of_day + timedelta(days=1)

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day.isoformat() + "Z",
        timeMax=end_of_day.isoformat() + "Z",
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    print("EVENTS:", events) 

    busy = []

    for event in events:
        if len(event) == 1:
            busy.append(event)
            break

        start_str = event['start'].get('dateTime')
        end_str = event['end'].get('dateTime')

        if not start_str or not end_str:
            continue

        try:
            start_str = start_str.replace("Z", "+00:00")
            end_str = end_str.replace("Z", "+00:00")

            event_start = datetime.fromisoformat(start_str)
            event_end = datetime.fromisoformat(end_str)

            # приводим к одной зоне (убираем tz)
            event_start = event_start.replace(tzinfo=None)
            event_end = event_end.replace(tzinfo=None)

            # проверка пересечения (ключ!)
            if event_end <= start_of_day or event_start >= end_of_day:
                continue

            actual_start = max(event_start, start_of_day)
            actual_end = min(event_end, end_of_day)

            # если занято весь день
            if actual_start == start_of_day and actual_end == end_of_day:
                return ["Весь день занят"]

            busy.append(
                f"{actual_start.strftime('%H:%M')} - {actual_end.strftime('%H:%M')}"
            )

        except Exception as e:
            print("ERROR:", e)

    return busy

# =====================
# HANDLERS - обрабатывает запрос и возвращает ответ
# =====================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Приветстую!\n"
        "Здесь информация о бронировании фотостудии\n\n"
        "Выбери действие кнопками",
        reply_markup=main_kb
    )
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    print(f"{name_db} активировала бот")

@dp.message(F.text == "📅 Проверить дату")
async def choose_date(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    write_log(f"{datetime.now()} | USER {name_db} | Проверить дату\n")
    print('\a')

    user_data[message.from_user.id] = {"state": "waiting_for_date"}
    await message.answer("Введите дату (DD.MM.YY)\nПример: 10.04.26")
    
    print(f'{name_db} нажала "📅 Проверить дату"')

@dp.message(F.text == "💳 Узнать стоимость")
async def cost(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    write_log(f"{datetime.now()} | USER {name_db} | Узнать стоимость\n")

    user_data[message.from_user.id] = {}
    await message.answer(
        "с 12:00 до 14:00 - 1800 рублей/час\n"
        "в остальное время - 2000 рублей/час\n"
        "фотостудия работает 24/7\n\n",
        reply_markup=main_kb
    )

@dp.message(F.text == "📟 Связаться с нами")
async def contact(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    write_log(f"{datetime.now()} | USER {name_db} | Связаться с нами\n")

    user_data[message.from_user.id] = {}
    await message.answer(
        "Администратор Венера: +7 (908) 26-19-471\n"
        "Написать нам в телеграм @sibirskaya_perm\n\n"
        "Наши соц. сети:\n"
        "https://vk.com/sibirskayaperm\n"
        "https://www.instagram.com/sibirskaya_perm/\n\n",
        reply_markup=main_kb
    )

@dp.message(F.text == "🛎️ Забронировать")
async def book(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    write_log(f"{datetime.now()} | USER {name_db} | Забронировать\n")

    await message.answer(
        "Для бронирования напишите нам в телеграм @sibirskaya_perm\n" \
        "или вконтакте https://vk.com/sibirskayaperm\n\n" \
    )

@dp.message(F.text == "↩️ Правила отмены бронирования")
async def cancellation_rules(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    write_log(f"{datetime.now()} | USER {name_db} | Правила отмены бронирования\n")
    
    photo = FSInputFile(BASE_DIR / "cancel.jpeg")
    await message.answer_photo(
        photo=photo,
        caption="",
        reply_markup=main_kb
    )
    photo = FSInputFile(BASE_DIR / "change.jpeg")
    await message.answer_photo(
        photo=photo,
        caption="",
        reply_markup=main_kb
    )

    
@dp.message(F.text)
async def handle_all(message: types.Message):
    user_id = message.from_user.id
    name_db = get_user_name(user_id) or user_id
    
    user_state = user_data.get(user_id, {}).get("state")

     # Словарь для корректного склонения месяцев
    MONTHS_RU = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
                7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    # ❗ игнорируем кнопки
    if message.text in [            
        "📅 Проверить дату",
        "🛎️ Забронировать",
        "📟 Связаться с нами",
        "💳 Узнать стоимость"
    ]:
        return

    # 👉 если ждём дату
    if user_state == "waiting_for_date":
        date_text = message.text.strip()

        write_log(f"{datetime.now()} | USER {name_db} | {date_text}\n")

        # ✅ проверка формата
        try:
            datetime.strptime(date_text, "%d.%m.%y")
        except ValueError:
            await message.answer(
                "⚠️ Введите дату в формате DD.MM.YY\nПример: 10.04.26"
            )
            print(f"{name_db} ввёла некорректную дату: {date_text}")
            return

        try:
            busy = get_busy_intervals(date_text)

            if busy == ['Весь день занят']:
                print("BUSY:", busy[0])
                reply = "День занят (нет свободного времени)"
            elif not busy:
                reply = "Свободно весь день!"
            else:
                reply = "Свободно:\n"
                print("BUSY:", busy)  # 
                current_time = "00:00"
                for interval in busy:
                    start, end = interval.split(" - ")
                    if current_time < start:
                        reply += f"{current_time} - {start}\n"
                    elif current_time == start:
                        pass  # нет свободного времени между интервалами
                    current_time = end
                if current_time != "00:00":
                    reply += f"{current_time} - 23:59\n"
            await message.answer(reply)
            print(f'{name_db} проверяет дату {date_text}\nПолучен ответ "{reply}"')

            # сброс состояния
            user_data[user_id] = {}

        except Exception as e:
            print("ERROR:", e)
            await message.answer("Ошибка при работе с календарём")
            write_log(f"{datetime.now()} | USER {name_db} | {date_text} дал ошибку: {e}\n")
            print('У {name_db} ошибка при работе с календарём:', e)

        return
       
    await message.answer("Выбери действие кнопками 👇") 


# =====================
# ЗАПУСК     # source venv/bin/activate из папки с venv
# =====================

async def main():
    print("=================================================")
    print("==============Клиентский бот запущен=============")
    print("=================================================")

    try:
        await dp.start_polling(bot)

    except Exception as e:
        print(f"Ошибка запуска: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
    
