import re
from datetime import datetime, date
from patients_tracker.database import DataBaseManager
from patients_tracker import structures

TIME_100_YEARS = 100 * 365.25 * 24 * 60 * 60
NAME_TEMPLATE = r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$'


def add_patient(fullname: str, date_of_birth: str) -> None:
    patient = structures.Patient(
        fullname=fullname,
        date_of_birth=datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
        time_of_visit=datetime.now()
    )

    with DataBaseManager() as db:
        db.add_new_patient(patient)
        return


def check_if_name_is_valid(fullname: str) -> bool:
    if re.match(NAME_TEMPLATE, fullname):
        return True

    return False


def check_if_date_is_valid(insert_date: str) -> bool:
    try:
        date = datetime.strptime(insert_date, "%Y-%m-%d")  # Format
        today = datetime.today()

        if date > today:  # Date of birth cannot be more than current date
            return False

        age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        if age >= 100:
            return False

        return True

    except ValueError:
        return False
