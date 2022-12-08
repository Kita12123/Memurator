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
    WARNING,
    CRITICAL
)

from ProgramData import DEBUG_LOG, INFO_LOG, WARNING_LOG, CRITICAL_LOG


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
    def handler_warning_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            WARNING_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(WARNING)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_critical_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            CRITICAL_LOG,
            mode="a",
            encoding="utf-8"
        )
        handler.setLevel(CRITICAL)
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
        logger.addHandler(self.handler_warning_file)
        logger.addHandler(self.handler_critical_file)
        return logger


class Log:

    def __init__(self):
        self.logger = LoggerDefine().logger

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def to_text_debug(self):
        with open(DEBUG_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

    def to_text_info(self):
        with open(INFO_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

    def to_text_warning(self):
        with open(WARNING_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

    def to_text_critical(self):
        with open(CRITICAL_LOG, mode="r", encoding="utf-8") as f:
            return f.readlines()

LOGGER = Log()