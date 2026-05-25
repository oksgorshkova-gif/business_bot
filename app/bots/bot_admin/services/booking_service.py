from app.bots.bot_admin.db.models import Booking, BookingUpdate
from app.bots.bot_admin.db.queries import insert_booking, get_event_id, delete_booking_from_bd
from app.bots.bot_admin.integrations.google_calendar import CALENDAR_ID, get_calendar_service

from datetime import datetime, timedelta


def create_booking(booking: Booking):

    service = get_calendar_service()

    name = booking.name
    start_datetime = booking.start_datetime
    end_datetime = booking.end_datetime
    comment = booking.comment
    type = booking.type
    price = booking.price

    try:
        event = {
                'summary': name,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Asia/Yekaterinburg'
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Asia/Yekaterinburg'
                },
                'description': f"{comment}" if comment else ""    
            }

            # Вставка в календарь
        created_event = service.events().insert(
            calendarId=CALENDAR_ID, 
            body=event).execute()
    
    except Exception as e:
        print(f"Ошибка при создании события в календаре:\n{e}")
        return
    
    insert_booking(start_datetime, end_datetime, type, price, created_event['id'], name, comment) 


def cleaning_service(start_datetime: datetime = None, end_datetime: datetime = None):

    if start_datetime:
        start_dt = start_datetime - timedelta(hours=1)
    else:
        start_dt = end_datetime
        
    ending = start_dt + timedelta(hours=1)
    booking = Booking(name="Уборка", start_datetime=start_dt, end_datetime=ending, type="service", price=0)
    create_booking(booking)


def update_booking(raw_text):

    info = BookingUpdate.parse_raw_text(raw_text)

    event_id = get_event_id(info.event_id)
    # взять event_id
    # обновить календарь
    # обновить БД


def deleted_event(booking_datetime):
    service = get_calendar_service()

    try:
        event_id = get_event_id(booking_datetime)
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f'Событие {event_id} удалено из календаря')
        delete_booking_from_bd(event_id)
        print(f'Событие {event_id} удалено из базы данных')
        return True
    except Exception as e:
        raise e
