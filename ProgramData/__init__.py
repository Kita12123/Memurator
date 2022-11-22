import os

SYSTEMDIR = os.path.dirname(__file__)

DATABASE = os.path.join(SYSTEMDIR, "database.db")
TEMP_CSV = os.path.join(SYSTEMDIR, "download.csv")
SYSTEM_JSON = os.path.join(SYSTEMDIR, "setting.json")
USER_JSON = os.path.join(SYSTEMDIR, "user.json")
DEBUG_LOG = os.path.join(SYSTEMDIR, "debug.txt")
INFO_LOG = os.path.join(SYSTEMDIR, "info.txt")
ERROR_LOG = os.path.join(SYSTEMDIR, "error.txt")