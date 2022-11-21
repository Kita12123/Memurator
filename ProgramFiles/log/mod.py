import os
from logging import (
    getLogger,
    StreamHandler,
    Formatter,
    FileHandler,
    Logger,
    DEBUG, INFO, ERROR
)

def create_logger(folder: str) -> Logger:
    LOGGER = getLogger(__name__)

    handler = StreamHandler()
    handler_file_error = FileHandler(
        os.path.join(folder, "error.txt"), mode="a",encoding="utf-8")
    handler_file_info  = FileHandler(
        os.path.join(folder, "info.txt"),  mode="a",encoding="utf-8")
    handler_file_debug = FileHandler(
        os.path.join(folder, "debug.txt"), mode="w",encoding="utf-8")

    handler.setLevel(DEBUG)
    handler_file_error.setLevel(ERROR)
    handler_file_info.setLevel(INFO)
    handler_file_debug.setLevel(DEBUG)
    LOGGER.setLevel(DEBUG)

    formatter = Formatter("[%(levelname)s]%(asctime)s-%(message)s")
    handler.setFormatter(formatter)
    handler_file_error.setFormatter(formatter)
    handler_file_info.setFormatter(formatter)
    handler_file_debug.setFormatter(formatter)

    LOGGER.addHandler(handler)
    LOGGER.addHandler(handler_file_error)
    LOGGER.addHandler(handler_file_info)
    LOGGER.addHandler(handler_file_debug)
    return LOGGER