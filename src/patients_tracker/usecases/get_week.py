from datetime import datetime, time, timedelta

from patients_tracker.database import DataBaseManager
from patients_tracker.usecases.errors import catch_date_errors


@catch_date_errors
def get_patients():
    today = datetime.today()
    weekday = today.weekday()

    patients = []

    with DataBaseManager() as db:
        for i in range(weekday + 1):  # +1 for current day
            day_date = today - timedelta(
                days=weekday - i
            )  # Iteration for all days at week
            start_of_day = datetime.combine(day_date, time.min)
            end_of_day = datetime.combine(day_date, time.max)
            patients.append(len(db.get_patients_by_time(start_of_day, end_of_day)))

    return patients
