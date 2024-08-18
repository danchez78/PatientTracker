from datetime import date, datetime
import sqlite3
from PatientsTracker.database import constants
from PatientsTracker import structures


class DataBaseManager:
    DB_LOCATION = "./patients.db"  # TODO: Environment variable

    def __init__(self):
        self.connection = sqlite3.connect(self.DB_LOCATION)
        self.cursor = self.connection.cursor()
        self._create_table()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def add_new_patient(self, patient_info: structures.Patient) -> None:
        self.cursor.execute(constants.INSERT_TABLE_COMMAND, patient_info.convert_to_tuple())

    def get_patients_by_time(self, start_date: date, end_date: date) -> list:
        return self.cursor.execute(constants.SELECT_PATIENTS_BY_VISIT_COMMAND, (start_date, end_date)).fetchall()

    def _create_table(self) -> None:
        self.cursor.execute(constants.CREATE_TABLE_COMMAND)


with DataBaseManager() as db:
    patient = structures.Patient(
        fullname="John",
        date_of_birth=date(year=2020, month=10, day=30),
        time_of_visit=datetime.now()
    )
    db.add_new_patient(patient)
    # a = db.get_patients_by_time(date(year=2000, month=10, day=30), datetime.now())
    # print(a)
    print(datetime.now().isocalendar())
