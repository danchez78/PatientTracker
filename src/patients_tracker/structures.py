from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Patient:
    fullname: str
    date_of_birth: date
    time_of_visit: datetime

    def convert_to_tuple(self) -> tuple:
        return self.fullname, self.date_of_birth, self.time_of_visit
