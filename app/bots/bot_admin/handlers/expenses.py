from app.bots.bot_admin.keyboards import main_kb
from app.bots.bot_admin.services.expenses_service import register_expense, register_mortgage_payment, register_mortgage_payment
from app.bots.bot_admin.services.report_service import get_profit, get_period, get_profit, get_range
from app.bots.bot_admin.states.auth_state import ExpenseState, MainMenuState, ReportState
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message

from app.bots.bot_admin.db.models import Spending

router = Router()

# @router.message(F.text == "Назад")
# async def back_handler(message: Message, state: FSMContext):
#     await state.clear()  # сбрасываем состояние

#     await message.answer(
#         "Главное меню:",
#         reply_markup=main_kb.main_kb()
#     )
#     await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(ExpenseState.waiting_write_expenses_type)
async def process_expense_category(message: Message, state: FSMContext):
    expense_category = message.text
    if expense_category == "Ипотека":
        register_mortgage_payment()
        await message.answer("Оплата ипотеки + КУ зарегистрирована.")
    elif expense_category == "КУ":
        await message.answer("Сумма\n[Комментарий]\n[DD.MM.YY]\n\n")
        await state.set_state(ExpenseState.waiting_write_ku_details)
    elif expense_category == "Прочее":
        await message.answer("Сумма\n[Комментарий]\n[DD.MM.YY]\n[extra-mortgage]\n\n")
        await state.set_state(ExpenseState.waiting_write_other_expenses_details)
    elif expense_category == "Назад":
        await message.answer(
            "Выбери действие:",
            reply_markup=main_kb.main_kb(),
        )
        await state.set_state(MainMenuState.waiting_reply_main_kb)
    else:
        await message.answer("Пожалуйста, выбери корректную категорию трат.")

@router.message(ExpenseState.waiting_write_ku_details)
async def process_ku_details(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        try:
            expense = Spending.parse_raw_text(raw_text)
            register_expense(amount=expense.amount, category="charges", comment=expense.comment, spending_date=expense.day)
            await message.answer("Коммунальные услуги зарегистрированы.")
        except Exception as e:
            print(f"Ошибка при обработке данных для КУ:\n{e}")
            await message.answer("❌ Пожалуйста, убедись, что формат правильный и попробуй снова.")
            await state.set_state(ExpenseState.waiting_write_ku_details)
            return
        
    await message.answer(
                "Выбери действие:",
                reply_markup=main_kb.main_kb(),
            )
    await state.set_state(MainMenuState.waiting_reply_main_kb) 


@router.message(ExpenseState.waiting_write_other_expenses_details)
async def process_other_expense_details(message: Message, state: FSMContext):
    raw_text = message.text
    if raw_text != "Назад":
        try:
            expense = Spending.parse_raw_text(raw_text)
            register_expense(amount=expense.amount, comment=expense.comment, spending_date=expense.day, category=expense.category)
            await message.answer("Трата зарегистрирована.")
        except Exception as e:
            await message.answer(f"❌ Ошибка {e}")
            await state.set_state(ExpenseState.waiting_write_other_expenses_details)
            return
        
    await message.answer(
                "Выбери действие:",
                reply_markup=main_kb.main_kb(),
            )
    await state.set_state(MainMenuState.waiting_reply_main_kb) 
