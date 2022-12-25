import os

import telebot
from telebot import types

from app import strings
from app.config import Commands, Paths, TGBot

bot = telebot.TeleBot(TGBot.TOKEN, parse_mode=None)

DOCUMENT_SEND_FLAG = "rb"


@bot.message_handler(commands=[Commands.START])
def start(message: types.Message):
    bot.send_message(message.chat.id, strings.START_RESPONSE)
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
    direction = [
        direction
        for direction in os.listdir(Paths.DIRECTIONS_PATH)
        if direction.lower() == choosen_direction.lower()
    ][0]
    direction_path = os.path.join(Paths.DIRECTIONS_PATH, direction)
    documents = tuple(
        open(os.path.join(direction_path, f), DOCUMENT_SEND_FLAG)
        for f in os.listdir(direction_path)
        if os.path.isfile(os.path.join(direction_path, f))
    )

    bot.send_message(
        message.chat.id,
        strings.SEND_DOCS_CAPTION,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    for doc in documents:
        bot.send_document(message.chat.id, document=doc)
