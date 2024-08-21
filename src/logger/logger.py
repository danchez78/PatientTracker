import logging
import os
import sys


class Logger:
    def __init__(self):
        filename = os.environ["LOG_FILE_LOCATION"]
        file_handler = logging.FileHandler(filename=filename, encoding="utf8")
        stdout_handler = logging.StreamHandler(stream=sys.stdout)

        logging.basicConfig(
            format="[%(asctime)s] [%(levelname)s] - %(message)s",
            handlers=[file_handler, stdout_handler],
        )
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        self.__logger = logger

    def debug(self, message: str) -> None:
        self.__logger.debug(message)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def critical(self, message: str) -> None:
        self.__logger.critical(message)
