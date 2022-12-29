"""
ログ管理
"""
from logging import (
    Formatter,
    FileHandler,
    StreamHandler,
    getLogger,
    DEBUG,
    ERROR,
    INFO,
)

from ProgramData import PROGRAM_DIR

INFO_FILE = PROGRAM_DIR / "info.txt"
ERROR_FILE = PROGRAM_DIR / "error.txt"

LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)

FORMAT = Formatter("[%(levelname)s]%(asctime)s-%(message)s")

handler_debug = StreamHandler()
handler_debug.setLevel(DEBUG)
handler_debug.setFormatter(FORMAT)

handler_info = FileHandler(INFO_FILE, mode="w", encoding="utf-8")
handler_info.setLevel(INFO)
handler_info.setFormatter(FORMAT)

handler_error = FileHandler(ERROR_FILE, mode="a", encoding="utf-8")
handler_error.setLevel(ERROR)
handler_error.setFormatter(FORMAT)

LOGGER.addHandler(handler_debug)
LOGGER.addHandler(handler_info)
LOGGER.addHandler(handler_error)


def get_info() -> str:
    with open(INFO_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def get_error() -> str:
    with open(ERROR_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    return text
