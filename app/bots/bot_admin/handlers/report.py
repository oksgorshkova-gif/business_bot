from app.bots.bot_admin.keyboards import main_kb
from app.bots.bot_admin.services.report_service import get_profit, get_period, get_profit, get_range, get_expences
from app.bots.bot_admin.states.auth_state import MainMenuState, ReportState
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Назад")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()  # сбрасываем состояние

    await message.answer(
        "Главное меню:",
        reply_markup=main_kb.main_kb()
    )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

@router.message(ReportState.waiting_reply_report_kb)
async def process_report_type(message: Message, state: FSMContext):
    report_type = message.text
    try:
        if report_type in ("Текущий месяц", "Следующий месяц"):
            period = get_period(report_type)
            profit = get_profit(period)
            expenses = get_expences(period)
            await message.answer(f"За {period[0].strftime('%d.%m.%Y')}-{period[1].strftime('%d.%m.%Y')}:\n"
                                f"Выручка {profit} руб.\n"
                                f"Траты {expenses} руб.\n"
                                f"Прибыль {profit-expenses} руб."
                                )            
        elif report_type == "Выбрать период":
            await message.answer("Введи период в формате\nДД.ММ.ГГ-ДД.ММ.ГГ")
            await state.set_state(ReportState.waiting_custom_period)
        elif report_type == "Назад":
            await message.answer(
                "Выбери действие:",
                reply_markup=main_kb.main_kb(),
            )
            await state.set_state(MainMenuState.waiting_reply_main_kb)
        else:
            await message.answer("Некорректный тип отчета.")

    except Exception as e:
        print(f"Ошибка при обработке запроса на отчет:\n{e}")
        await message.answer("Произошла ошибка при получении отчета. {e}")
        await state.set_state(ReportState.waiting_reply_report_kb)

@router.message(ReportState.waiting_custom_period)
async def process_custom_period(message: Message, state: FSMContext):
    report_range = message.text.strip()
    try:
        get_range_result = get_range(report_range)
        date_start, date_end = get_range_result
        profit = get_profit((date_start, date_end))
        expenses = get_expences((date_start, date_end))
        await message.answer(f"За {date_start.strftime('%d.%m.%Y')}-{date_end.strftime('%d.%m.%Y')}:\n"
                             f"Выручка {profit} руб.\n"
                             f"Траты {expenses} руб.\n"
                             f"Прибыль {profit-expenses} руб."
                             )
    except Exception as e:
        print(f"Ошибка при обработке пользовательского периода:\n{e}")
        await message.answer("❌ Произошла ошибка при обработке введенного периода. Пожалуйста, убедись, что формат правильный и попробуй снова.")
        await state.set_state(ReportState.waiting_custom_period)
        return
    
    await message.answer(
                "Выбери действие:",
                reply_markup=main_kb.main_kb(),
            )
    await state.set_state(MainMenuState.waiting_reply_main_kb)

