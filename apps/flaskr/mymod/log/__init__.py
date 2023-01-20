"""
ログ管理
"""
from logging import DEBUG, getLogger

from apps.flaskr.mymod.log.handler import Handler
from ProgramData import CRITICAL_LOG, DEBUG_LOG, INFO_LOG, WARNING_LOG


class Log:

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.setLevel(DEBUG)
        handler = Handler()
        self.logger.addHandler(handler.default)
        self.logger.addHandler(handler.debug_file)
        self.logger.addHandler(handler.info_file)
        self.logger.addHandler(handler.warning_file)
        self.logger.addHandler(handler.critical_file)

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
