from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.types import FSInputFile, KeyboardButton

# =====================
# KEYBOARDS
# =====================

def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Забронировать")], # -> booking_kb()   
            [KeyboardButton(text="Изменить бронирование")], # -> booking_update_kb
            [KeyboardButton(text="Отчет")], # -> report_kb
            [KeyboardButton(text="Записать трату")], # -> expenses_kb
            [KeyboardButton(text="Заготовленные ответы")], # -> reply_kb
            [KeyboardButton(text="Обновить код")], # -> waiting_for_new_code = State()
            [KeyboardButton(text="/start")],
        ],
        resize_keyboard=True, 
    input_field_placeholder="Выбери 👇"
)   
#============ БРОНИРОВАНИЕ =================
def booking_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Авито бронирование")], # state -> waiting_raw_text_avito
            [KeyboardButton(text="Суточно бронирование")], # state -> waiting_raw_text_sutochno
            [KeyboardButton(text="Фотосессии")], # state -> waiting_raw_text_hourly
            [KeyboardButton(text="Закрыть для бронирования")],
            [KeyboardButton(text="Назад")], # state -> waiting_reply_main_kb
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
    )   

def booking_update_kb(): # waiting_update_booking_type
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить")], # waiting_update_info
            [KeyboardButton(text="Отменить")], # waiting_cancel_info
            [KeyboardButton(text="Назад")],
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)
#============ ОТЧЕТЫ =================
def report_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Текущий месяц")], # state -> waiting_reply_report_kb 
            [KeyboardButton(text="Следующий месяц")], # state -> waiting_reply_report_kb
            [KeyboardButton(text="Выбрать период")], # state -> waiting_custom_period
            [KeyboardButton(text="Назад")], # state -> waiting_reply_main_kb
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)   
#============ ЗАГОТОВЛЕННЫЕ ОТВЕТЫ =================
def reply_kb():
    return ReplyKeyboardMarkup( 
        keyboard=[
            [KeyboardButton(text="Суточные")], # state -> waiting_messages_daily
            [KeyboardButton(text="Фотосессии")], # state -> waiting_messages_hourly
            [KeyboardButton(text="Назад")], # state -> waiting_reply_main_kb
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)

def hourly_messages_kb():
    return ReplyKeyboardMarkup( 
        keyboard=[
            [KeyboardButton(text="Суточные")], # state -> waiting_messages_daily
            [KeyboardButton(text="Фотосессии")], # state -> waiting_messages_hourly
            [KeyboardButton(text="Назад")], # state -> waiting_reply_main_kb
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)

def reply_hourly_kb():
    return ReplyKeyboardMarkup( 
        keyboard=[
            [KeyboardButton(text="Полное")], 
            [KeyboardButton(text="Только код, заходите раньше")],
            [KeyboardButton(text="Ключи дать другим гостям")], 
            [KeyboardButton(text="До вас другие гости")],
            [KeyboardButton(text="Назад")], 
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)

def reply_daily_kb():
    return ReplyKeyboardMarkup( 
        keyboard=[
            [KeyboardButton(text="Спасибо, оплачивайте")],
            [KeyboardButton(text="Сколько вас")], 
            [KeyboardButton(text="День заезда")],
            [KeyboardButton(text="День заезда без камеры")], 
            [KeyboardButton(text="Назад")], 
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)


#============ ТРАТЫ =================

def expenses_type_kb():
    return ReplyKeyboardMarkup( 
        keyboard=[
            [KeyboardButton(text="Ипотека")], 
            [KeyboardButton(text="КУ")],
            [KeyboardButton(text="Прочее")],
            [KeyboardButton(text="Назад")], # state -> waiting_reply_main_kb
            ],
        resize_keyboard=True,
    input_field_placeholder="Выбери 👇"
)