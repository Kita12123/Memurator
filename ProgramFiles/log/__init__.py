""" 
Define logging module as LOGGER
"""
from functools import wraps
import traceback

from ProgramData import SYSTEMDIR
from ProgramFiles.log import mod

LOGGER = mod.create_logger(
    folder=SYSTEMDIR
)

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