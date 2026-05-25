from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from app.bots.bot_admin.services.auth_service import check_password
from app.bots.bot_admin.states.auth_state import AuthState

router = Router()


@router.message(AuthState.waiting_password)
async def process_password(message: Message, state: FSMContext):
    if check_password(message.from_user.id, message.text):
        await message.answer("✅ Доступ открыт")
        await state.clear()
    else:
        await message.answer("❌ Неверный пароль")
