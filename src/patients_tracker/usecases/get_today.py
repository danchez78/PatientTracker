from datetime import datetime, time

from patients_tracker import structures
from patients_tracker.database import DataBaseManager
from patients_tracker.usecases.errors import catch_date_errors


@catch_date_errors
def get_patients() -> list:
    patients = []
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    with DataBaseManager() as db:

        for patient in db.get_patients_by_time(start_of_day, end_of_day):
            patients.append(
                structures.Patient(
                    fullname=patient[0],
                    date_of_birth=datetime.strptime(patient[1], "%Y-%m-%d"),
                    time_of_visit=datetime.strptime(patient[2], "%Y-%m-%d %H:%M:%S.%f"),
                )
            )

    return patients
