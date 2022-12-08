"""
ログ管理モジュール
"""
from logging import (
    getLogger,
    StreamHandler,
    Formatter,
    FileHandler,
    Logger,
    DEBUG,
    INFO,
    ERROR,
)

from ProgramData import DEBUG_LOG, INFO_LOG, ERROR_LOG


class LoggerDefine:
    """logger作成"""

    def __init__(self):
        self.formater = Formatter("[%(levelname)s]%(asctime)s-%(message)s")

    @property
    def handler_default(self) -> StreamHandler:
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_debug_file(self) -> FileHandler:
        """Output debug.txt"""
        handler = FileHandler(
            DEBUG_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_info_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            INFO_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(INFO)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_error_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            ERROR_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(ERROR)
        handler.setFormatter(self.formater)
        return handler

    @property
    def logger(self) -> Logger:
        """"""
        logger = getLogger("__main__")
        logger.setLevel(DEBUG)
        logger.addHandler(self.handler_default)
        logger.addHandler(self.handler_debug_file)
        logger.addHandler(self.handler_info_file)
        logger.addHandler(self.handler_error_file)
        return logger


class Log:

    def __init__(self):
        self.logger = LoggerDefine().logger

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    @property
    def text_oneline(self):
        with open(INFO_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()[-1:]

    @property
    def text_debug(self):
        with open(DEBUG_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

    @property
    def text_info(self):
        with open(INFO_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

    @property
    def text_error(self):
        with open(ERROR_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

LOGGER = Log()