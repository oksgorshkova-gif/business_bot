import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


def _getenv(name: str, default: str | None = None, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


ADMIN_BOT_TOKEN = _getenv("ADMIN_BOT_TOKEN") or _getenv("BOT_TOKEN")
CLIENT_BOT_TOKEN = _getenv("CLIENT_BOT_TOKEN")

DB_HOST = _getenv("DB_HOST", "localhost")
DB_PORT = int(_getenv("DB_PORT", "5432"))
DB_NAME = _getenv("DB_NAME", "postgres")
DB_USER = _getenv("DB_USER", "postgres")
DB_PASSWORD = _getenv("DB_PASSWORD", "")

CALENDAR_ID = _getenv("CALENDAR_ID")
_service_account_file = _getenv("GOOGLE_SERVICE_ACCOUNT_FILE") or _getenv("SERVICE_ACCOUNT_FILE")
if _service_account_file:
    service_account_path = Path(_service_account_file)
    if not service_account_path.exists() and not service_account_path.is_absolute():
        project_root = Path(__file__).resolve().parent.parent
        for candidate in (
            project_root / service_account_path,
            project_root / "app" / "bots" / "bot_clients" / service_account_path,
            project_root / "app" / "bots" / "bot_admin" / service_account_path,
        ):
            if candidate.exists():
                service_account_path = candidate
                break
    GOOGLE_SERVICE_ACCOUNT_FILE = str(service_account_path)
else:
    GOOGLE_SERVICE_ACCOUNT_FILE = None
GOOGLE_SERVICE_ACCOUNT_JSON = _getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
PASSWORD = _getenv("PASSWORD", "")

LOG_FILE = _getenv("LOG_FILE", "/app/logs/logs.txt")

MONTHS_RU = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
                7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

months = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
    }
