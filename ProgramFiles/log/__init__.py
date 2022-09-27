""" 
Define logging module as LOGGER
"""
# 2022.08.19 作成
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, INFO, ERROR
from functools import wraps
import os
import traceback

CD = os.path.dirname(__file__)
LOGGER = getLogger(__name__)

handler = StreamHandler()
handler_file_error = FileHandler(os.path.join(CD, "error.txt"),mode="a",encoding="utf-8")
handler_file_info  = FileHandler(os.path.join(CD, "info.txt" ),mode="a",encoding="utf-8")
handler_file_debug = FileHandler(os.path.join(CD, "debug.txt"),mode="w",encoding="utf-8")

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



# デコレータ - プログラムの開始、終了をログで表示
def dec_display_doc(function):
    """Decorater : Display start, ended of function

    Args:
        function (Obj): function of target
    """
    @wraps(function)
    def wrapped(*args,**kwargs):
        line = "="*10
        LOGGER.debug(f"{line} START {function.__doc__} {line}")
        result = function(*args,**kwargs)
        LOGGER.debug(f"{line} ENDED {function.__doc__} {line}")
        return result
    return wrapped

def dsp_except():
    LOGGER.critical(traceback.format_exc())