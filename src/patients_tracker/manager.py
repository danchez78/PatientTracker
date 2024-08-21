import functools
import os

from telebot import TeleBot, types

from logger import Logger

from . import database, errors, structures, usecases

logger = Logger()

token = os.environ["BOT_TOKEN"]
tb = TeleBot(token)

patient_data = {}

commands = [
    types.BotCommand(command="start", description="Запустить бота"),
    types.BotCommand(command="add", description="Добавить пациента"),
    types.BotCommand(
        command="list_today", description="Получить список пациентов за сегодня"
    ),
    types.BotCommand(
        command="list_week", description="Получить список пациентов за эту неделю"
    ),
]
tb.set_my_commands(commands)


def start():
    tb.infinity_polling()


def catch_errors(func):
    @functools.wraps(func)
    def function_wrapper(message: types.Message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except (ConnectionError, database.errors.OperationalError) as exc:
            error = errors.ConnectError(info=f"{exc}")
            logger.error(error.info)
        except database.errors.DatabaseInteractionError as exc:
            error = errors.DatabaseError(message=exc.message, info=exc.info)
            logger.error(f"{error.message}: {error.info}")
        except usecases.errors.DateError as exc:
            error = errors.AppError(message=exc.message, info=exc.info)
            logger.error(f"{error.message}: {error.info}")
        except Exception as exc:
            error = errors.AppError(
                message="Unknown error occurred. Investigations is recommended.",
                info=f"{exc}",
            )
            logger.error(f"{error.message}: {error.info}")

        tb.send_message(message.chat.id, error.info)
        raise error

    return function_wrapper


@tb.message_handler(commands=["start"])
@catch_errors
def _cmd_start(message: types.Message):
    logger.info(f"Called `start` command from user with ID `{message.from_user.id}`")

    tb.send_message(
        message.chat.id,
        "<b>/add</b> - Добавить пациента\n"
        "<b>/list_today</b> - Получить список пациентов за сегодня\n"
        "<b>/list_week</b> - Получить список пациентов за эту неделю\n"
        "Команды всегда доступны в меню",
        parse_mode="HTML",
    )


@tb.message_handler(commands=["add"])
@catch_errors
def _add_patient(message: types.Message):
    logger.info(f"Called `add` command from user with ID `{message.from_user.id}`")

    sent = tb.send_message(
        message.chat.id,
        "Введите ФИО пациента в формате <b>Фамилия Имя Отчество</b>\n",
        parse_mode="HTML",
    )
    patient_data[message.from_user.id] = {}
    tb.register_next_step_handler(sent, _get_patient_name)


@tb.message_handler(commands=["list_today"])
@catch_errors
def _get_patients_today(message: types.Message):
    logger.info(
        f"Called `list_today` command from user with ID `{message.from_user.id}`"
    )

    patients = []
    for patient in usecases.get_today.get_patients():
        patients.append(patient.to_str())
    patients_msg = "Список пациентов за сегодня:\n" + "".join(patients)

    logger.info(f"Get patients for week result: `{patients_msg}`")

    tb.send_message(message.chat.id, patients_msg)


@tb.message_handler(commands=["list_week"])
@catch_errors
def _get_patients_for_week(message: types.Message):
    logger.info(
        f"Called `list_week` command from user with ID `{message.from_user.id}`"
    )

    week = usecases.get_week.get_patients()

    patients_msg = "Список пациентов за эту неделю:\n"
    i = 0
    for day in week:
        patients_msg += f"{structures.WEEKDAYS[i]} - {day}\n"
        i += 1

    logger.info(f"Get patients for week result: `{patients_msg}`")

    tb.send_message(message.chat.id, patients_msg)


def _get_patient_name(message: types.Message):
    if message.text == "/break":
        logger.warning("User cancelled entering patient name")
        tb.send_message(message.chat.id, "Добавление нового пациента отменено. \n")
        return

    valid_status = usecases.add_patient.check_if_name_is_valid(message.text)
    if valid_status == structures.StatusOfValidation.Valid:
        logger.info(f"Name `{message.text}` passed validation successfully")
        sent = tb.send_message(
            message.chat.id,
            "Введите дату рождения в формате <b>yyyy-mm-dd</b>\n",
            parse_mode="html",
        )
        patient_data[message.from_user.id]["name"] = message.text
        tb.register_next_step_handler(sent, _get_patient_birth)

    else:
        logger.warning(f"Name `{message.text}` failed to pass validation")
        sent = tb.send_message(
            message.chat.id,
            "ФИО введены некорректно. \n"
            f"Ошибка: {valid_status.value}\n"
            "Вводите <b>без</b> специальных символов, цифр и пробелов. \n"
            "Пример: <b>Иванов Иван Иванович</b>\n"
            "Попробуйте еще раз. Для того, чтобы отменить ввод введите <b>/break</b>\n",
            parse_mode="html",
        )
        tb.register_next_step_handler(sent, _get_patient_name)


def _get_patient_birth(message: types.Message):
    if message.text == "/break":
        logger.info("User cancelled entering patient birth")
        tb.send_message(message.chat.id, "Добавление нового пациента отменено. \n")
        return

    valid_status = usecases.add_patient.check_if_date_is_valid(message.text)
    if valid_status == structures.StatusOfValidation.Valid:
        logger.info(f"Birth `{message.text}` passed validation successfully")
        patient_data[message.from_user.id]["date"] = message.text
        _save_patient(message)

    else:
        logger.warning(f"Birth `{message.text}` failed to pass validation")
        sent = tb.send_message(
            message.chat.id,
            "Дата введена некорректно. \n"
            f"Ошибка: {valid_status.value}\n"
            "Вводите <b>без</b> специальных символов, букв и пробелов.\n"
            "Пример: <b>2024-8-19</b>\n"
            "Попробуйте еще раз. Для того, чтобы отменить ввод введите <b>/break</b>\n",
            parse_mode="html",
        )
        tb.register_next_step_handler(sent, _get_patient_birth)


def _save_patient(message: types.Message) -> None:
    patient_name = patient_data[message.from_user.id]["name"]
    patient_birth = patient_data[message.from_user.id]["date"]

    logger.info(
        f"Saving patient with name `{patient_name}` and birth `{patient_birth}`"
    )

    usecases.add_patient.add_patient(patient_name, patient_birth)

    logger.info(f"Patient saved successfully")

    del patient_data[message.from_user.id]
    tb.send_message(message.chat.id, "Пациент успешно добавлен!")
    return
