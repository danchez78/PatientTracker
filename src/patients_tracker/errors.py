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
