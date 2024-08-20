import functools
from sqlite3 import DatabaseError, OperationalError, ProgrammingError


class DatabaseInteractionError(Exception):
    """Base exception for database level"""

    def __init__(self, message: str, info: str):
        self.message = message
        self.info = info


class DatabaseConnectionError(DatabaseInteractionError):
    """The error is raised when an unexpected shutdown occurred, independent of the work of the project."""

    def __init__(self, info: str):
        self.message = "An unexpected connection error was received. The request should be repeated."
        self.info = info


class DatabaseCodeError(DatabaseInteractionError):
    """The error is raised when there is a problem with the table, parameters, or SQL syntax"""

    def __init__(self, info: str):
        self.message = "An unexpected error in the code. An investigation is required."
        self.info = info


def catch_database_errors(func):
    @functools.wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as exc:
            raise DatabaseConnectionError(f"{exc}")
        except ProgrammingError as exc:
            raise DatabaseCodeError(f"{exc}")
        except DatabaseError as exc:
            raise DatabaseInteractionError(
                message="An unknown database error was received.",
                info=f"{exc}"
            )

    return function_wrapper
