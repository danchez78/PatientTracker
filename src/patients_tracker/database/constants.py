TABLE_NAME = "Patients"
CREATE_TABLE_COMMAND = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fullname TEXT NOT NULL,
date_of_birth DATE,
time_of_visit DATE
)
"""

INSERT_TABLE_COMMAND = f"""
INSERT INTO {TABLE_NAME} (fullname, date_of_birth, time_of_visit) VALUES (?, ?, ?)
"""

SELECT_PATIENTS_BY_VISIT_COMMAND = f"""
SELECT fullname, date_of_birth, time_of_visit FROM {TABLE_NAME} WHERE time_of_visit BETWEEN (?) and (?)
"""
