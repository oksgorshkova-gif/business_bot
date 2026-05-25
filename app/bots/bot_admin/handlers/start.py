from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.bots.bot_admin.keyboards import main_kb
from app.bots.bot_admin.services.auth_service import check_password, is_authorized

from app.bots.bot_admin.states.auth_state import AuthState, BookingState, ExpenseState, MainMenuState, MessageState, ReportState, KeyboxState

router = Router()
user_data = {}


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    if not is_authorized(message.from_user.id):
        print(message.from_user.id)
        await message.answer(
            "Введи пароль:"
        )
        await state.set_state(AuthState.waiting_password)
    else:
        await message.answer(
            "Вы уже авторизованы. Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(AuthState.waiting_password)
async def main_menu_handler(message: Message, state: FSMContext):
    if check_password(message.from_user.id, message.text):
        await state.clear()
        await message.answer("✅ Доступ открыт")
        await message.answer(
        "Выбери действие:",
        reply_markup=main_kb.main_kb(),
    )
        await state.set_state(MainMenuState.waiting_reply_main_kb)

    else:
        await message.answer("❌ Неверный пароль")


@router.message(MainMenuState.waiting_reply_main_kb)
async def process_booking_type(message: Message, state: FSMContext):
    booking_type = message.text
    if booking_type == "Забронировать":
        await message.answer("Выбери тип бронирования:", reply_markup=main_kb.booking_kb())
        await state.set_state(BookingState.waiting_booking_type)  
    elif booking_type == "Изменить бронирование":
        await message.answer("Выбери тип изменения:", reply_markup=main_kb.booking_update_kb())
        await state.set_state(BookingState.waiting_update_booking_type)
    elif booking_type == "Отчет":
        await message.answer("Выбери тип отчета:", reply_markup=main_kb.report_kb())
        await state.set_state(ReportState.waiting_reply_report_kb)
    elif booking_type == "Записать трату":
        await message.answer("Выбери тип траты:", reply_markup=main_kb.expenses_type_kb())
        await state.set_state(ExpenseState.waiting_write_expenses_type)
    elif booking_type == "Заготовленные ответы":
        await message.answer("Выбери категорию заготовленных ответов:", reply_markup=main_kb.reply_kb())
        await state.set_state(MessageState.waiting_messages_reply_kb)
    elif booking_type == "Обновить код":
        await message.answer("Диктуй:")
        await state.set_state(KeyboxState.waiting_for_new_code)
    elif booking_type == "Обновить бот":
        await state.clear()
        await message.answer(
            "Возобновлено",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer("Пожалуйста, выбери корректное действие.")
