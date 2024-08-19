import os

from telebot import TeleBot, types
from patients_tracker import usecases, structures


token = os.getenv("BOT_TOKEN")
tb = TeleBot(token)
patient_data = {}

commands = [
    types.BotCommand(command='start', description='Запустить бота'),
    types.BotCommand(command='add', description='Добавить пациента'),
    types.BotCommand(command='list_today', description='Получить список пациентов за сегодня'),
    types.BotCommand(command='list_week', description='Получить список пациентов за эту неделю'),
]
tb.set_my_commands(commands)


def start():
    tb.infinity_polling()


@tb.message_handler(commands=["start"])
def _cmd_start(message: types.Message):
    tb.send_message(message.chat.id, "/add - Добавить пациента\n"
                                     "/list_today - Получить список пациентов за сегодня\n"
                                     "/list_week - Получить список пациентов за эту неделю\n"
                                     "Команды всегда доступны в меню")


@tb.message_handler(commands=["add"])
def _add_patient(message: types.Message):
    sent = tb.send_message(message.chat.id, "Введите ФИО пациента в формате Фамилия Имя Отчество\n")
    patient_data[message.from_user.id] = {}
    tb.register_next_step_handler(sent, _get_patient_name)


@tb.message_handler(commands=["list_today"])
def _get_patients_today(message: types.Message):
    patients = []
    for patient in usecases.get_today.get_patients():
        patients.append(patient.to_str())
    patients_msg = "Список пациентов за сегодня:\n" + "".join(patients)
    tb.send_message(message.chat.id, patients_msg)


@tb.message_handler(commands=["list_week"])
def _get_patients_for_week(message: types.Message):
    week = usecases.get_week.get_patients()
    patients_msg = "Список пациентов за эту неделю:\n"
    i = 0
    for day in week:
        patients_msg += f"{structures.WEEKDAYS[i]} - {day}\n"
    tb.send_message(message.chat.id, patients_msg)


def _get_patient_name(message: types.Message):
    if message.text == "/break":
        tb.send_message(message.chat.id, "Добавление нового пациента отменено. \n")
        return

    if usecases.add_patient.check_if_name_is_valid(message.text):
        sent = tb.send_message(message.chat.id, "Введите дату рождения в формате yyyy-mm-dd\n")
        patient_data[message.from_user.id]["name"] = message.text
        tb.register_next_step_handler(sent, _get_patient_birth)

    else:
        sent = tb.send_message(message.chat.id, "ФИО введены некорректно. \n"
                                                "Вводите без специальных символов, цифр и пробелов. \n"
                                                "Дата должна быть существующей и не позднее сегодняшнего дня. \n"
                                                "Пример: Иванов Иван Иванович\n"
                                                "Попробуйте еще раз. Для того, чтобы отменить ввод введите /break\n")
        tb.register_next_step_handler(sent, _get_patient_name)


def _get_patient_birth(message: types.Message):
    if message.text == "/break":
        tb.send_message(message.chat.id, "Добавление нового пациента отменено. \n")
        return

    if usecases.add_patient.check_if_date_is_valid(message.text):
        patient_data[message.from_user.id]["date"] = message.text
        _save_patient(message)

    else:
        sent = tb.send_message(message.chat.id, "Дата введена некорректно. \n"
                                                "Вводите без специальных символов, букв и пробелов.\n"
                                                "Пример: 2024-8-19\n"
                                                "Попробуйте еще раз. Для того, чтобы отменить ввод введите /break\n")
        tb.register_next_step_handler(sent, _get_patient_birth)


def _save_patient(message: types.Message) -> None:
    usecases.add_patient.add_patient(
        patient_data[message.from_user.id]["name"],
        patient_data[message.from_user.id]["date"]
    )
    del patient_data[message.from_user.id]
    tb.send_message(message.chat.id, "Пациент успешно добавлен!")
    return
