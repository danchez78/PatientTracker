import os

from telebot import TeleBot, types


token = os.environ.get("BOT_TOKEN")


tb = TeleBot(token)


def start():
    tb.infinity_polling()


@tb.message_handler(commands=["start"])
def _cmd_start(message: types.Message):
    tb.send_message(message.chat.id, "/add - Добавить пациента\n"
                                    "/list_today - Список пациентов за сегодня\n"
                                    "/list_week - Список пациентов за неделю")


@tb.message_handler(commands=["add"])
def _add_patient(message: types.Message):
    sent = tb.send_message(message.chat.id, "Введите ФИО пациента")
    tb.register_next_step_handler(sent, _save_patient)


@tb.message_handler(commands=["list_today"])
def _get_patients_today(message: types.Message):
    patients = ["Сидоров Олег Петрович", "Смирнова Олеся Викторовна"]
    patients_msg = "Список пациентов за сегодня:\n" + "\n".join(patients)
    tb.send_message(message.chat.id, patients_msg)


@tb.message_handler(commands=["list_week"])
def _get_patients_for_week(message: types.Message):
    patients = ["Сидоров Олег Петрович", "Смирнова Олеся Викторовна"]
    patients_msg = "Список пациентов за эту неделю:\n" + "\n".join(patients)
    tb.send_message(message.chat.id, patients_msg)


def _save_patient(message: types.Message):
    patient_name = message.text
    # TODO: saving ...
    tb.send_message(message.chat.id, f"ФИО {patient_name} успешно сохранено")
