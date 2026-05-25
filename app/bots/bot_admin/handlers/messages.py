from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bots.bot_admin.db.queries import get_last_keybox_code
from app.bots.bot_admin.keyboards import main_kb

from app.bots.bot_admin.states.auth_state import MainMenuState, MessageState

router = Router()

@router.message(MessageState.waiting_messages_reply_kb)
async def process_messages_reply_kb(message: Message, state: FSMContext):
    reply_type = message.text
    if reply_type == "Суточные":
        await state.set_state(MessageState.waiting_messages_daily)
        await message.answer("Выбери тип сообщения", reply_markup=main_kb.reply_daily_kb())
    elif reply_type == "Фотосессии":
        await state.set_state(MessageState.waiting_messages_hourly)
        await message.answer("Выбери тип сообщения", reply_markup=main_kb.reply_hourly_kb())
    elif reply_type == "Назад":
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer("Пожалуйста, выбери корректную категорию заготовленных ответов.")

@router.message(MessageState.waiting_messages_hourly)
async def process_messages_hourly(message: Message, state: FSMContext):
    reply = message.text
    code = get_last_keybox_code()
    if reply == "Полное":
        await message.answer(
                            ", здравствуйте!\n\n"
                            "Вам оставили ключ в верхнем сейфе на подъездной двери." 
                            "После съемки его нужно будет туда же вернуть "
                            "(сбейте пароль когда закроете сейф, чтобы его не смогли открыть другие люди).\n\n"
                            f"Пароль {code}.\n\n"
                            "Внутри подъезда правая дверь, пароль от нее \"3\". 2-ой этаж, белая дверь. \n\n"
                            "Можете заходить раньше и тогда раньше закончите 🤗"
        )
    elif reply == "Только код, заходите раньше":
        await message.answer(
                            f"Пароль {code}.\n\n"
                            "Можете заходить раньше и тогда раньше закончите 🤗"
        )
    elif reply == "Ключи дать другим гостям":
        await message.answer(
                            ", здравствуйте!\n\n"
                            "Вам оставят ключ в верхнем сейфе на подъездной двери. "
                            "После съемки его нужно будет передать следующим гостям. Они подойдут к \n\n"
                            "Или вернуть ключи в сейф.\n\n"
                            f"Пароль {code}."
        )
    elif reply == "До вас другие гости":
        await message.answer(
                            ", здравствуйте!\n\n"
                            "Ждем Вас сегодня к . Пожалуйста, не приходите раньше, до Вас съемка.\n\n"
                            "Вам передадут ключи, после съемки их нужно будет вернуть в верхний сейф на уличной двери.\n\n"
                            f"Пароль {code}."
        )
    elif reply == "Назад":
        await message.answer(
            "Выбери категорию заготовленных ответов:",
            reply_markup=main_kb.reply_kb(),
        )
        await state.set_state(MessageState.waiting_messages_reply_kb)
    else:
        await message.answer("Пожалуйста, выбери корректный тип ответа.")
    
    await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(MessageState.waiting_messages_daily)
async def process_messages_hourly(message: Message, state: FSMContext):
    reply = message.text
    code = get_last_keybox_code()
    if reply == "Спасибо, оплачивайте":
        await message.answer(
            "Здравствуйте! Благодарю за интерес к нашей квартире. "
            "Для подтверждения бронирования необходимо внести предоплату."
        )
    elif reply == "Сколько вас":
        await message.answer(
            "Уточните, пожалуйста, время заезда, выезда и количество гостей.\n"
            "Сайт часто ошибочно выдает информацию"
        )
    elif reply == "День заезда":
        await message.answer(
            "Здравствуйте, !\n\n"
            "Ждем Вас завтра у нас в квартире с 9:00. "
            "📍Сибирская 1, 1 подъезд. кв 6. Пароль от правой двери внутри подъезда «3». 2-ой этаж. Белая дверь.\n\n"
            "Ключи оставим для Вас в верхнем сейфе на уличной двери. 1-ый подъезд.\n\n"
            f"Пароль от сейфа {code}.\n\n"
            "Как зайдете, пожалуйста, доплатите +3000 (залог) на сбер +79223676156 Оксана Андреевна.\n\n"
            "В углу напротив входа есть камера, ее можно сразу выключить при входе в квартиру. "
            "Там выведен выключатель внизу камеры. "
            "Тогда при выезде её нужно будет включить обратно.\n\n" 
            "WiFi\nимя MTSRouter _5G_94C9\nпароль 18546699"
        )
    elif reply == "День заезда без камеры":
        await message.answer(
            "Здравствуйте, !\n\n"
            f"Пароль от сейфа {code}.\n\n"
            "Как зайдете, пожалуйста, доплатите +3000 (залог) на сбер +79223676156 Оксана Андреевна.\n\n"
            "WiFi\nимя MTSRouter _5G_94C9\nпароль 18546699"
        )
    elif reply == "Назад":
        await message.answer(
            "Выбери категорию заготовленных ответов:",
            reply_markup=main_kb.reply_kb(),
        )
        await state.set_state(MessageState.waiting_messages_reply_kb)
    else:
        await message.answer("Пожалуйста, выбери корректный тип ответа.")
    
    await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
    await state.set_state(MainMenuState.waiting_reply_main_kb)
    
