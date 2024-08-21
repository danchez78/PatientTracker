import re
from datetime import datetime

from patients_tracker import structures
from patients_tracker.database import DataBaseManager
from patients_tracker.usecases.errors import catch_date_errors

TIME_100_YEARS = 100 * 365.25 * 24 * 60 * 60
NAME_TEMPLATE = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$"


@catch_date_errors
def add_patient(fullname: str, date_of_birth: str) -> None:
    patient = structures.Patient(
        fullname=fullname,
        date_of_birth=datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
        time_of_visit=datetime.now(),
    )

    with DataBaseManager() as db:
        db.add_new_patient(patient)
        return


def check_if_name_is_valid(fullname: str) -> structures.StatusOfValidation:
    if re.match(NAME_TEMPLATE, fullname):
        return structures.StatusOfValidation.Valid

    return structures.StatusOfValidation.InvalidNameFormat


@catch_date_errors
def check_if_date_is_valid(insert_date: str) -> structures.StatusOfValidation:
    try:
        date = datetime.strptime(insert_date, "%Y-%m-%d")  # Format
        today = datetime.today()

        if date > today:  # Date of birth cannot be more than current date
            return structures.StatusOfValidation.InvalidDateValue

        age = (
            today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        )
        if age >= 100:
            return structures.StatusOfValidation.InvalidAge

        return structures.StatusOfValidation.Valid

    except ValueError:
        return structures.StatusOfValidation.InvalidDateFormat
