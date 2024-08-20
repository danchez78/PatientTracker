import functools
from patients_tracker.database import errors as database_errors
from patients_tracker.usecases import errors as date_errors


class AppError(Exception):
    """Base exception for app level"""
    def __init__(self, message: str, info: str):
        self.message = message
        self.info = info


class ConnectError(AppError):
    """Exception for connection errors"""
    def __init__(self, info: str):
        self.message = "An error occurred with the connection"
        self.info = info


class DatabaseError(AppError):
    """Exception for database errors"""
    def __init__(self, message: str, info: str):
        self.message = message
        self.info = info


def catch_errors(func):
    @functools.wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError | database_errors.OperationalError as exc:
            raise ConnectError(info=f"{exc}")
        except database_errors.DatabaseInteractionError as exc:
            raise DatabaseError(message=exc.message, info=exc.info)
        except date_errors.DateError as exc:
            raise AppError(message=exc.message, info=exc.info)
        except Exception as exc:
            raise AppError(message="Unknown error occurred. Investigations is recommended.", info=f"{exc}")

    return function_wrapper
