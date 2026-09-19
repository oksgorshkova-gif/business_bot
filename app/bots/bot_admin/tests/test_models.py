import pytest
from datetime import datetime
from app.bots.bot_admin.db.models import Booking

class TestBookingFromTextAvito:

    def test_full_valid_input(self):
        """Тест с полным набором данных: имя, даты с временем, цена и комментарий."""
        text = """Иван Иванов
                15.05.2024 15:30
                17.05.2024 11:00
                5500
                Поздний заезд, есть кот
                """
        
        booking = Booking.from_text_avito(text)
        
        assert booking.name == "Иван Иванов"
        assert booking.start_datetime == datetime(2024, 5, 15, 15, 30)
        assert booking.end_datetime == datetime(2024, 5, 17, 11, 0)
        assert booking.price == 5500
        assert booking.comment == "Поздний заезд, есть кот"
        assert booking.type == "daily" # Значение по умолчанию

    def test_input_without_time_and_comment(self):
        """Тест без указания времени (должно подставиться 14:00 и 12:00) и без комментария."""
        text = """
                Петр Петров
                20.06.2024
                22.06.2024
                3000
                """
                        
        booking = Booking.from_text_avito(text)
        
        assert booking.name == "Петр Петров"
        # Проверяем, что время заезда подставилось как 14:00
        assert booking.start_datetime == datetime(2024, 6, 20, 14, 0)
        # Проверяем, что время выезда подставилось как 12:00
        assert booking.end_datetime == datetime(2024, 6, 22, 12, 0)
        assert booking.price == 3000
        assert booking.comment is None

    def test_invalid_date_format(self):
        """Тест с некорректным форматом даты. Должен вызвать ValueError."""
        text = """Сидоров
                invalid_date_string
                22.06.2024
                1000"""
                        
        with pytest.raises(ValueError, match="Не удалось распарсить даты бронирования"):
            Booking.from_text_avito(text)

    def test_invalid_price_format(self):
        """Тест с некорректной ценой (не число). Должен вызвать ValueError (из-за int())."""
        text = """Гость
                20.06.2024
                22.06.2024
                тысяча"""
        
        # int() выбросит ValueError, если строку нельзя преобразовать в число
        with pytest.raises(ValueError):
            Booking.from_text_avito(text)

    def test_input_with_extra_newlines(self):
        """Тест проверяет, что метод корректно обрабатывает лишние пробелы/переносы в начале и конце."""
        text = """
                Мария Смирнова
                10.10.2024 16:00
                12.10.2024 10:00
                4000
                Комментарий

                """
        # text.strip() в начале метода уберет лишние переносы
        booking = Booking.from_text_avito(text.strip())
        
        assert booking.name == "Мария Смирнова"
        assert booking.price == 4000