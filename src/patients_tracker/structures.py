from dataclasses import dataclass
from datetime import date, datetime

WEEKDAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


@dataclass
class Patient:
    fullname: str
    date_of_birth: date
    time_of_visit: datetime

    def to_tuple(self) -> tuple:
        return self.fullname, self.date_of_birth, self.time_of_visit

    def to_str(self) -> str:
        return f"\nФИО: {self.fullname}\n" \
               f"Дата рождения: {self.date_of_birth.strftime('%Y-%m-%d')}\n" \
               f"Время посещения: {self.time_of_visit.strftime('%Y-%m-%d %H:%M')}\n"
