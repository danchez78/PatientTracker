import os
import sqlite3
from datetime import date

from patients_tracker.database import constants
from patients_tracker.database.errors import catch_database_errors
from patients_tracker import structures


class DataBaseManager:
    DB_LOCATION = os.getenv("DB_LOCATION")

    def __init__(self):
        self.connection = sqlite3.connect(self.DB_LOCATION)
        self.cursor = self.connection.cursor()
        self._create_table()  # Checking for the existence of a table is inserted into the sql command

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

    @catch_database_errors
    def add_new_patient(self, patient_info: structures.Patient) -> None:
        self.cursor.execute(constants.INSERT_TABLE_COMMAND, patient_info.to_tuple())

    @catch_database_errors
    def get_patients_by_time(self, start_date: date, end_date: date) -> list:
        return self.cursor.execute(constants.SELECT_PATIENTS_BY_VISIT_COMMAND, (start_date, end_date)).fetchall()

    @catch_database_errors
    def _create_table(self) -> None:
        self.cursor.execute(constants.CREATE_TABLE_COMMAND)
