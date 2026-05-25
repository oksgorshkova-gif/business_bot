from dataclasses import dataclass
from datetime import datetime, timedelta, date
import dateparser

@dataclass
class Booking: 
    name: str
    start_datetime: datetime
    end_datetime: datetime
    price: int
    type: str = "daily"
    place: str = "Sibirskaya"
    comment: str = None


    @classmethod   
    def from_text_sutochno(cls, text: str):
        """
        parsing from sutochno_bot
        """

        start_dt = None
        end_dt = None
        price = 0
        name = "Unknown"
        comment = []

        lines = text.strip().split("\n")
        for line in lines:
            if line.startswith("➡️ Заезд"):
                start_dt = dateparser.parse(line.split("➡️ Заезд")[1].strip(),languages=["ru"], settings={"DATE_ORDER": "DMY"})
            elif line.startswith("⬅️️ Отъезд"):
                end_dt = dateparser.parse(line.split("⬅️️ Отъезд")[1].strip(),languages=["ru"], settings={"DATE_ORDER": "DMY"})
            elif line.startswith("Оплата"):
                price = int(line.split("Оплата при заселении составит")[1].strip().replace("₽.", ""))
            elif line.startswith("📞"):
                name = f"{line.split("—")[1].split()[0].strip()} суточно"
        comment = "\n".join(lines[6:])

        #print("name=", name, "start_datetime=", start_dt, "end_datetime=", end_dt, "price=", price, "comment=", comment)

        # Проверка, что даты распарсились
        if not start_dt or not end_dt:
            raise ValueError("Не удалось распарсить даты бронирования")

        return cls(name=name, start_datetime=start_dt, end_datetime=end_dt, price=price, comment=comment)
    
    @classmethod
    def from_text_avito(cls, text: str):
        """
        parsing from avito
        """
        start_dt = None
        end_dt = None
        price = 0
        name = "Unknown"
        comment = []

        lines = text.strip().split("\n")
        name = lines[0]

        raw_start = lines[1]
        if ":" not in raw_start:
            raw_start += " 14:00"
        start_dt = dateparser.parse(
            raw_start,
            languages=["ru"],
            settings={"DATE_ORDER": "DMY"}
        )

        raw_end = lines[2]
        if ":" not in raw_end:
            raw_end += " 12:00"
        end_dt = dateparser.parse(
            raw_end,
            languages=["ru"],
            settings={"DATE_ORDER": "DMY"}
        )

        price = int(lines[3])
        comment = lines[4] if len(lines) > 4 else None

        # Проверка, что даты распарсились
        if not start_dt or not end_dt:
            raise ValueError("Не удалось распарсить даты бронирования")

        return cls(name=name, start_datetime=start_dt, end_datetime=end_dt, price=price, comment=comment)
    
    @classmethod
    def from_text_hourly(cls, text: str):
        """
        parsing from hourly
        """
        start_dt = None
        end_dt = None
        price = 0
        name = "Unknown"
        comment = []

        name, date_str, time_str, delta, price, *comment = [p.strip() for p in text.strip().split("\n")]

        print("начало парсинга")    
        # Парсинг даты и времени
        date_event = datetime.strptime(date_str, "%d.%m.%y")
        time_start = datetime.strptime(time_str, "%H:%M").time()
        start_dt = datetime.combine(date_event, time_start)
        print("парсинг даты и времени успешен")
        # Парсинг длительности
        if ":" in delta:
            hours, minutes = map(int, delta.split(":"))
        else:
            hours, minutes = int(delta), 0

        actual_duration = timedelta(hours=hours, minutes=minutes)
        prep_time = timedelta(minutes=15)
        end_dt = start_dt + actual_duration + prep_time

        # Проверка, что даты распарсились
        if not start_dt or not end_dt:
            raise ValueError("Не удалось распарсить даты бронирования")

        print("парсинг длительности успешен")
        return cls(name=name, start_datetime=start_dt, end_datetime=end_dt, price=price, comment=comment, type="hourly")

@dataclass
class Spending:

    amount: int
    day: datetime
    category: str
    comment: str = None

    @classmethod
    def parse_raw_text(cls, text: str):

        amount = 0
        comment = ''
        day = None
        category = None
        
        try:
            text_parts = text.split("\n")
            amount = int(text_parts[0].strip())
            comment = text_parts[1].strip() if len(text_parts) > 1 else ""
            date_str = text_parts[2].strip() if len(text_parts) > 2 else ""
            day = datetime.strptime(date_str, "%d.%m.%y") if date_str else date.today()

            if len(text_parts) != 4:
                category = "extra"
            elif len(text_parts) == 4:
                category = "extra-mortgage"
        
            print("парсинг даты успешен")
            return cls(amount=amount, comment=comment, day=day, category=category)
        except Exception as e:
            print(f"Ошибка в Spending.parse_raw_text\n {e}")
            raise e

@dataclass        
class BookingUpdate:
    old_datetime: datetime
    new_datetime: datetime | None
    price_delta: int | None
    return_all_money: bool
    comment: str = 'перенесенное'

    @classmethod
    def parse_raw_text(cls, text: str):
        old_dt = None
        new_dt = None
        return_amount = 0
        money_all = False

        try:
            parts = text.split("\n")
            old_date = datetime.strptime(parts[0].strip(), "%d.%m.%y")
            old_time = datetime.strptime(parts[1].strip(), "%H:%M").time()
            old_dt = datetime.combine(old_date, old_time)

            if len(parts) == 3: # отмена 
                if parts[2].lower() == 'нет':
                    money_all = False
                elif parts[2].lower() == 'да':
                    money_all = True
                else:
                    raise ValueError('Непонятно делать ли возврат гостю')
                
            else: #перенос
                new_date = datetime.strptime(parts[2].strip(), "%d.%m.%y")
                new_time = datetime.strptime(parts[3].strip(), "%H:%M").time()
                new_dt = datetime.combine(new_date, new_time)
                if len(parts) == 5:
                    return_amount = int(parts[4])
            return cls(old_datetime=old_dt, new_datetime=new_dt, return_all_money=money_all, price_delta=return_amount)
        
        except Exception as e:
            print(f'Ошибка при парсинге: {e}')
            raise e




async def update_price_delta(pool, booking_id: int, delta: int):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE bookings 
            SET price = price + $1 
            WHERE id = $2
            """,
            delta,       # Здесь может быть и 10, и -10
            booking_id
        )

                    
                    




            