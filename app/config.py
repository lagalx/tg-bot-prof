import os
from enum import auto

from strenum import LowercaseStrEnum, StrEnum


class EnvKeys(StrEnum):
    BOT_TOKEN = auto()
    BASE_PATH = auto()
    DIRECTIONS_DIR = auto()


class TGBot(StrEnum):
    TOKEN: str = os.getenv(EnvKeys.BOT_TOKEN)


class Commands(LowercaseStrEnum):
    START = auto()


class Paths(StrEnum):
    BASE_PATH: str = os.path.abspath(os.getenv(EnvKeys.BASE_PATH))
    DIRECTIONS_DIR: str = os.getenv(EnvKeys.DIRECTIONS_DIR)
    DIRECTIONS_PATH: str = os.path.join(BASE_PATH, DIRECTIONS_DIR)
