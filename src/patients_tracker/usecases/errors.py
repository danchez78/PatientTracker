import functools


class DateError(Exception):
    """Base exception for working with dates"""
    def __init__(self, info: str):
        self.message = "An unknown error occurred while working with the date format"
        self.info = info


def catch_date_errors(func):
    @functools.wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            raise DateError(info=f"{exc}")

    return function_wrapper
