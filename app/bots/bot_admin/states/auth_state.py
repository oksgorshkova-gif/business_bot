from aiogram.fsm.state import State, StatesGroup

class AuthState(StatesGroup):
    waiting_password = State()
    waiting_for_new_code = State()


class MainMenuState(StatesGroup):
    waiting_reply_main_kb = State()

class BookingState(StatesGroup):
    waiting_raw_text_sutochno = State()
    waiting_raw_text_hourly = State()
    waiting_raw_text_avito = State()
    waiting_booking_type = State()

    waiting_update_booking_type = State()
    waiting_update_info = State()
    waiting_cancel_info = State()

class ReportState(StatesGroup):
    waiting_reply_report_kb = State()
    waiting_custom_period = State()
    preparing_report_current_month = State()
    preparing_report_previous_month = State()
    preparing_report = State()

class ExpenseState(StatesGroup):
    waiting_reply_expenses_type = State()
    waiting_write_expenses_type = State()
    waiting_read_expenses_type = State()
    waiting_write_ku_details = State()
    waiting_write_other_expenses_details = State()

class MessageState(StatesGroup):
    waiting_messages_reply_kb = State()
    waiting_messages_daily = State()
    waiting_messages_hourly = State()

class KeyboxState(StatesGroup):
    waiting_keybox_code = State()
    waiting_for_new_code = State()