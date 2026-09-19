import pytest
from datetime import datetime, timedelta
from app.bots.bot_admin.db.models import Booking  

class TestBookingFromTextHourly:

    def test_valid_input_with_colon_duration_and_comment(self):
        """Тест: стандартный ввод, длительность в формате ЧЧ:ММ, есть комментарий."""
        text = """Иван Иванов
15.05.24
14:00
1:30
2500
Нужен чайник"""
        
        booking = Booking.from_text_hourly(text)
        
        assert booking.name == "Иван Иванов"
        assert booking.start_datetime == datetime(2024, 5, 15, 14, 0)
        # 1 час 30 мин + 15 мин подготовка = 1 час 45 мин
        assert booking.end_datetime == datetime(2024, 5, 15, 15, 45)
        assert booking.price == '2500'
        assert booking.comment == ["Нужен чайник"] # Обратите внимание: это список!
        assert booking.type == "hourly"

    def test_valid_input_with_dot_duration(self):
        """Тест: длительность в формате дробного числа с точкой (1.5 часа = 1ч 30м)."""
        text = """Петр Петров
20.06.24
10:00
1.5
1500"""
        
        booking = Booking.from_text_hourly(text)
        
        assert booking.name == "Петр Петров"
        assert booking.start_datetime == datetime(2024, 6, 20, 10, 0)
        # 1.5 часа (90 мин) + 15 мин подготовка = 105 мин = 1 час 45 мин
        assert booking.end_datetime == datetime(2024, 6, 20, 11, 45)
        assert booking.price == '1500'
        assert booking.comment == [] # Комментария нет, распаковка *comment дает пустой список

    def test_valid_input_with_comma_duration(self):
        """Тест: длительность в формате дробного числа с запятой (2,5 часа = 2ч 30м)."""
        text = """Анна Сидорова
01.01.25
18:00
2,5
3000"""
        
        booking = Booking.from_text_hourly(text)
        
        assert booking.start_datetime == datetime(2025, 1, 1, 18, 0)
        # 2.5 часа (150 мин) + 15 мин подготовка = 165 мин = 2 часа 45 мин
        assert booking.end_datetime == datetime(2025, 1, 1, 20, 45)
        assert booking.price == '3000'

    def test_valid_input_with_integer_duration(self):
        """Тест: длительность в формате целого числа (2 часа)."""
        text = """Сергей
10.10.24
12:00
2
2000"""
        
        booking = Booking.from_text_hourly(text)
        
        assert booking.start_datetime == datetime(2024, 10, 10, 12, 0)
        # 2 часа (120 мин) + 15 мин подготовка = 135 мин = 2 часа 15 мин
        assert booking.end_datetime == datetime(2024, 10, 10, 14, 15)
        assert booking.price == '2000'

    def test_invalid_date_format(self):
        """Тест: некорректный формат даты должен вызывать ValueError."""
        text = """Гость
invalid_date
14:00
1
1000"""
        
        with pytest.raises(ValueError):
            Booking.from_text_hourly(text)

    def test_invalid_time_format(self):
        """Тест: некорректный формат времени должен вызывать ValueError."""
        text = """Гость
15.05.24
25:99
1
1000"""
        
        with pytest.raises(ValueError):
            Booking.from_text_hourly(text)

    def test_not_enough_lines(self):
        """Тест: если строк меньше 5, распаковка переменных вызовет ValueError."""
        text = """Гость
15.05.24
14:00""" # Нет длительности, цены и комментария
        
        with pytest.raises(ValueError):
            Booking.from_text_hourly(text)