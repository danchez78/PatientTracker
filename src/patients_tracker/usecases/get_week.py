from datetime import datetime, timedelta
from patients_tracker.database import DataBaseManager


def get_patients():
    # Получаем текущую дату и день недели
    today = datetime.today()
    weekday = today.weekday()  # 0 - понедельник, 1 - вторник, ..., 6 - воскресенье

    # Список для хранения дат
    patients = []

    with DataBaseManager() as db:
        for i in range(weekday + 1):  # +1, чтобы включить сегодняшний день
            day_date = today - timedelta(days=weekday - i)
            start_of_day = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = day_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            patients.append(len(db.get_patients_by_time(start_of_day, end_of_day)))

    return patients

