import os

import patients_tracker
from logger import Logger

logger = Logger()


def main():
    logger.info("Bot is started")

    patients_tracker.start()

    logger.info("Bot is stopped")


if __name__ == "__main__":
    main()

    os._exit(1)  # noqa
