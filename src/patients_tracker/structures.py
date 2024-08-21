from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum

WEEKDAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]


class StatusOfValidation(StrEnum):
    Valid = ""
    InvalidNameFormat = "Данные введены в неправильном формате."
    InvalidDateFormat = "Данные введены в неправильном формате."
    InvalidDateValue = "Дата не может быть позднее сегодняшнего дня."
    InvalidAge = "Возраст пациента не может быть более 100 лет."


@dataclass
class Patient:
    fullname: str
    date_of_birth: date
    time_of_visit: datetime

    def to_tuple(self) -> tuple:
        return self.fullname, self.date_of_birth, self.time_of_visit

    def to_str(self) -> str:
        return (
            f"\nФИО: {self.fullname}\n"
            f"Дата рождения: {self.date_of_birth.strftime('%Y-%m-%d')}\n"
            f"Время посещения: {self.time_of_visit.strftime('%Y-%m-%d %H:%M')}\n"
        )
