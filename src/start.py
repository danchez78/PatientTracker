import os

import patients_tracker


if __name__ == "__main__":
    print("Bot is started")

    patients_tracker.start()

    print("Bot is stopped")

    os._exit(1) # noqa