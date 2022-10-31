import os

cd = os.path.dirname(__file__)
DATABASE = os.path.join(cd, "database.db")
TEMP_CSV = os.path.join(cd, "download.csv")
SETTING_JSON = os.path.join(cd, "setting.json")
USER_JSON = os.path.join(cd, "user.json")
DEBUG_LOG = os.path.join(cd, "debug.txt")
INFO_LOG = os.path.join(cd, "info.txt")
ERROR_LOG = os.path.join(cd, "error.txt")