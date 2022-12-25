import os

from telebot import types

from app.constants import DOCUMENT_SEND_FLAG


def media_docs_from_files(path):
    result = tuple(
        types.InputMediaDocument(open(os.path.join(path, f), DOCUMENT_SEND_FLAG))
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    )
    return result
