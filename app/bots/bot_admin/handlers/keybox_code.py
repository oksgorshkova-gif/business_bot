from aiogram import Router, F, Dispatcher
from app.bots.bot_admin.keyboards.main_kb import main_kb
from app.bots.bot_admin.states.auth_state import KeyboxState, MainMenuState
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bots.bot_admin.db.queries import set_keybox_codes


router = Router()
dp = Dispatcher()



#========================
# KEYBOX
#========================

@router.message(KeyboxState.waiting_for_new_code)
async def text_handler(message: Message, state: FSMContext):
    try:
        new_code = message.text.strip()

    except ValueError:
        await message.answer("❌ Код должен быть числом")
        return
    set_keybox_codes(new_code)
    await message.answer("✅ Код обновлен")

    await message.answer(
        "Выбери действие:",
        reply_markup=main_kb(),
    )

    await state.set_state(MainMenuState.waiting_reply_main_kb)
