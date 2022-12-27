import os

import telebot
from telebot import types

from app import strings
from app.config import Commands, Paths, TGBot
from app.constants import MAX_MEDIA_GROUP_LEN
from app.tg_utils import media_docs_from_files
from app.types import User
from app.utils import partition

bot = telebot.TeleBot(TGBot.TOKEN, parse_mode=None)


@bot.message_handler(commands=[Commands.START])
def start(message: types.Message):
    bot.send_message(message.chat.id, strings.START_RESPONSE)
    bot.send_message(message.chat.id, strings.REQUEST_USER_NAME)
    bot.register_next_step_handler(message, request_user_name)


def request_user_name(message: types.Message):
    fio = message.text.split()
    if len(fio) != 3:
        bot.send_message(message.chat.id, strings.ERROR_FIO_NOT_FULL)
        bot.register_next_step_handler(message, request_user_name)
        return

    last_name, first_name, middle_name = fio
    user = User(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
    )
    choose_direction(message)


def choose_direction(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
        one_time_keyboard=True,
        input_field_placeholder=strings.CHOOSE_DIRECTION,
    )

    for direction in os.listdir(Paths.DIRECTIONS_PATH):
        button = types.KeyboardButton(direction.capitalize())
        markup.add(button)

    bot.send_message(
        message.chat.id,
        text=strings.CHOOSE_DIRECTION,
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, send_docs)


def send_docs(message: types.Message):
    choosen_direction = message.text
    try:
        direction = [
            direction
            for direction in os.listdir(Paths.DIRECTIONS_PATH)
            if direction.lower() == choosen_direction.lower()
        ][0]
    except:
        bot.send_message(message.chat.id, strings.ERROR_FIND_DIRECTION)
        bot.register_next_step_handler(message, send_docs)
        return
    direction_path = os.path.join(Paths.DIRECTIONS_PATH, direction)
    documents = media_docs_from_files(direction_path)

    bot.send_message(
        message.chat.id,
        strings.SEND_DOCS_CAPTION,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    for docs_part in partition(documents, MAX_MEDIA_GROUP_LEN):
        bot.send_media_group(message.chat.id, media=docs_part)
