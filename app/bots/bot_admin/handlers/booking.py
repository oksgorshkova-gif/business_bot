from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.config import MONTHS_RU
from app.bots.bot_admin.db.models import Booking, BookingUpdate
from app.bots.bot_admin.services.booking_service import deleted_event
from app.bots.bot_admin.keyboards import main_kb
from app.bots.bot_admin.services.booking_service import create_booking, cleaning_service
from app.bots.bot_admin.services.reminders_service import format_timedelta
from app.bots.bot_admin.states.auth_state import BookingState, MainMenuState


router = Router()

@router.message(BookingState.waiting_booking_type)
async def process_booking_type(message: Message, state: FSMContext):
    booking_type = message.text
    if booking_type == "Суточно бронирование":
        await state.set_state(BookingState.waiting_raw_text_sutochno)
        await message.answer("Введи данные из суточно бот")
    elif booking_type == "Авито бронирование":
        await state.set_state(BookingState.waiting_raw_text_avito)
        await message.answer(f"Имя\n"
                            f"Дата DD.MM.YY и время (если не 14:00) заезда\n"
                            f"Дата и время (если не 12:00) отъезда\n"
                            f"Стоимость\n"
                            f"Комментарий (необязательно)")
    elif booking_type == "Фотосессии":
        await state.set_state(BookingState.waiting_raw_text_hourly)
        await message.answer(f"Имя\n"
                            f"Дата DD.MM.YY\n"
                            f"Время начала HH:MM\n"
                            f"Длительность (в формате HH:ММ или в часах)\n"
                            f"Стоимость\n"
                            f"Комментарий (необязательно)")
    elif booking_type == "Закрыть для бронирования":
        await message.answer("Функция для закрытия бронирования пока не реализована.")
    elif booking_type == "Назад":
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer("Пожалуйста, выбери корректный тип бронирования.")
    
@router.message(BookingState.waiting_raw_text_sutochno)
async def process_sutochno_text(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        await state.clear()
        await message.answer(f"Начинаю обработку\n")
        try:
            booking =  Booking.from_text_sutochno(raw_text)
            
        except Exception as e:
            print(f"Ошибка при обработке:\n{e}")
            await message.answer(f"❌ Ошибка при обработке\n{e}")
            return
        await message.answer(f"✅ Обработка текста успешна\n")

        cleaning_service(start_datetime=booking.start_datetime)
        create_booking(booking)
        cleaning_service(end_datetime=booking.end_datetime)

        await message.answer(f"✅ Бронирование успешно создано\n\n")
        await message.answer(f"✅ Уборка добавлена\n\n")
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    else:
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

    
@router.message(BookingState.waiting_raw_text_avito)
async def process_avito_text(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        await state.clear()
        await message.answer(f"Начинаю обработку\n")
    
        try:
            booking = Booking.from_text_avito(raw_text)
        except Exception as e:
            print(f"Ошибка при обработке:\n{e}")
            await message.answer(f"❌ Ошибка при обработке\n\n{e}")
            return
        await message.answer(f"✅ Обработка текста успешна\n\n")
        
        cleaning_service(booking.start_datetime)
        create_booking(booking)
        cleaning_service(booking.end_datetime)

        await message.answer(f"✅ Бронирование успешно создано\n\n")
        await message.answer(f"✅ Уборка добавлена\n\n")

        await message.answer(
            f"Здравствуйте! Благoдарю за бронирование.\n"
            f"Ждём Вас {booking.start_datetime.day} {MONTHS_RU[booking.start_datetime.month]} "
            f"с {booking.start_datetime.strftime('%H:%M')}. "
            f"Выезд {booking.end_datetime.day} {MONTHS_RU[booking.end_datetime.month]} "
            f"до {booking.end_datetime.strftime('%H:%M')}.\n\n"
            f"📍 Сибирская 1, 1 подъезд, кв 6.\n"
            f"Пароль от правой двери внутри подъезда «3». 2-ой этаж, белая дверь.\n\n"
            f"Ключи оставим для Вас в верхнем сейфе на уличной двери. 1-ый подъезд.\n\n"
            f"Актуальный пароль пришлем в день заезда.\n\n"
            )
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )

        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)



@router.message(BookingState.waiting_raw_text_hourly)
async def process_hourly_text(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        await state.clear()
        await message.answer(f"Начинаю обработку\n")
        try:
            booking = Booking.from_text_hourly(raw_text)
        except Exception as e:
            print(f"Ошибка при обработке:\n{e}")
            await message.answer(f"❌ Ошибка при обработке\n\n{e}")
            return

        create_booking(booking)
        await message.answer(
                    f"Забронировали!\n"
                    f"Ждём Вас {booking.start_datetime.day} {MONTHS_RU[booking.start_datetime.month]} в {booking.start_datetime.strftime('%H:%M')}–{booking.end_datetime.strftime('%H:%M')}.\n\n"
                    f"📍 Сибирская 1, 1 подъезд, кв 6.\n"
                    f"Пароль от правой двери внутри подъезда «3». 2-ой этаж, белая дверь.\n\n"
                    f"⏳ Фактическое время аренды {format_timedelta(booking.end_datetime - booking.start_datetime)}.\n"
                    f"Время на вход и выход (15 мин) уже включено в общее время.\n"
                    f"В квартире можно находиться только в забронированное время.\n\n"
                    f"После фотосессии верните, пожалуйста, квартиру в изначальное состояние.\n\n"
                    f"Экстренная связь Венера 89082619471"
        )
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)
    
    
#===========ИЗМЕНЕНИЕ БРОНИРОВАНИЯ============

@router.message(BookingState.waiting_update_booking_type)
async def process_update_booking_type(message: Message, state: FSMContext):
    booking_type = message.text
    if booking_type == "Изменить":
        await state.set_state(BookingState.waiting_update_info)
        await message.answer(
                            "Старые данные, новые данные[, изменение стоимости]:\n"
                            "DD.MM.YY\n"
                            "HH:MM\n"
                            "DD.MM.YY\n"
                            "HH:MM\n"
                            "[+/-amount]")
    elif booking_type == "Отменить":
        await state.set_state(BookingState.waiting_cancel_info)
        await message.answer(
                            "Данные, возврат клиенту\n"
                            "DD.MM.YY\n"
                            "HH:MM\n"
                            "да/нет")
    else:
        #booking_type == "Назад":
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(BookingState.waiting_update_info)
async def update_avito(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        await state.clear()
        await message.answer(f"Начинаю обработку\n")
        success = update_event(raw_text)
        if success:
            await message.answer(f"✅ Событие удалено")
        else:
            await message.answer(f"❌ Ошибка при обработке")
        

        #await message.answer(
            # f"Здравствуйте! Благoдарю за бронирование.\n"
            # f"Ждём Вас {booking.start_datetime.day} {MONTHS_RU[booking.start_datetime.month]} с {booking.start_datetime.strftime('%H:%M')}. Выезд {booking.end_datetime.day} {MONTHS_RU[booking.end_datetime.month]} до {booking.end_datetime.strftime('%H:%M')}.\n\n"
            # f"📍 Сибирская 1, 1 подъезд, кв 6.\n"
            # f"Пароль от правой двери внутри подъезда «3». 2-ой этаж, белая дверь.\n\n"
            # f"Ключи оставим для Вас в верхнем сейфе на уличной двери. 1-ый подъезд.\n\n"
            # f"Актуальный пароль пришлем в день заезда.\n\n"
            # )
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(BookingState.waiting_cancel_info)
async def delete_avito(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        await state.clear()
        await message.answer(f"Начинаю обработку\n")
        booking = BookingUpdate.parse_raw_text(raw_text)
        success = deleted_event(booking.old_datetime)
        if success:
            await message.answer(f"✅ Событие удалено")
        else:
            await message.answer(f"❌ Ошибка при обработке")
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

    
