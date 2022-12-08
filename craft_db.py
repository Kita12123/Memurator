"""
データベース作成
"""
from ProgramFiles.db.file_ins import TOTAL_SYUKA
from ProgramFiles.db.sql_ins import DB_SQL
from ProgramFiles.flaskr.mymod.log import LOGGER, dsp_except

#
# Main Function
#
def main(
    first_yyyy:str,
    last_yyyy :str
    ):
    first_yyyy = int(first_yyyy)
    last_yyyy  = int(last_yyyy)
    yyyy = first_yyyy
    while True:
        TOTAL_SYUKA.refresh(
            where=f"伝票日付>={yyyy - 1950}0000 AND 伝票日付<={yyyy - 1950}9999"
        )
        if yyyy == last_yyyy:
            break
        else:
            yyyy += 1

if __name__=="__main__":
    first_yyyy = 2000
    last_yyyy = 2020
    DB_SQL.db_open()
    try:
        LOGGER.info(f"*************** Start Connect HOST and SQL ({first_yyyy} - {last_yyyy}) ***************")
        main(
            first_yyyy=first_yyyy,
            last_yyyy =last_yyyy
        )
    except:
        dsp_except()
    DB_SQL.db_close()