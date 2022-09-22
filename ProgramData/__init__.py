import os

cd = os.path.dirname(__file__)
DATABASE = os.path.join(cd, "database.db")
TEMP_CSV = os.path.join(cd, "download.csv")
HOST_ODBC_STRINGS = "DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
M_SETTING_PATH = os.path.join(cd, "setting.json")