import json

from googleapiclient.discovery import build
from google.oauth2 import service_account

from app import config

# =====================
# GOOGLE CALENDAR API SETUP
# =====================
SCOPES = config.SCOPES
SERVICE_ACCOUNT_FILE = config.GOOGLE_SERVICE_ACCOUNT_FILE
SERVICE_ACCOUNT_JSON = config.GOOGLE_SERVICE_ACCOUNT_JSON

def get_calendar_service():
    if SERVICE_ACCOUNT_JSON:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(SERVICE_ACCOUNT_JSON),
            scopes=SCOPES,
        )
    elif SERVICE_ACCOUNT_FILE:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )
    else:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SERVICE_ACCOUNT_FILE is required")

    service = build('calendar', 'v3', credentials=credentials)
    return service

CALENDAR_ID = config.CALENDAR_ID
# =====================

def create_event(event_data):
    service = get_calendar_service()
    return service.events().insert(
        calendarId=CALENDAR_ID,
        body=event_data
    ).execute()

def delete_event(event_id): 
    service = get_calendar_service()
    return service.events().delete(
        calendarId=CALENDAR_ID,
        eventId=event_id
    ).execute()

def update_event(event_id, event_data):
    service = get_calendar_service()
    return service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=event_data
    ).execute()
