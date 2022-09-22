"""
データベース作成
引数
    1: 開始日付 (デフォルト - 2000)
    2: 終了日付（デフォルト - 現在)
注意
    MUJNRPFの別のクエリを実行中だと
    pyodbc.Error: ('HY000', 'The driver did not supply an error!')
    が出力されて、エラーになる可能性がある。
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

from ProgramFiles.db import file_ins
from ProgramFiles.log import LOGGER, dsp_except

#
# Main Function
#
def main(
    first_yyyy:str,
    last_yyyy :str
    ):
    if first_yyyy == "":
        first_yyyy = "1990"
    if last_yyyy  == "":
        last_yyyy  = datetime.today().strftime(r"%Y")
    first_yyyy = int(first_yyyy)
    last_yyyy  = int(last_yyyy)
    yyyy = first_yyyy
    while True:
        file_ins.TOTAL_URI.refresh(
            sql=f"伝票日付>={yyyy - 1950}0000 AND 伝票日付<={yyyy - 1950}9999"
        )
        if yyyy == last_yyyy:
            break
        else:
            yyyy += 1

if __name__=="__main__":
    try:
        first_yyyy = sys.argv[1]
    except(IndexError):
        first_yyyy = ""
    try:
        last_yyyy = sys.argv[2]
    except(IndexError):
        last_yyyy = ""
    try:
        LOGGER.info(f"*************** Start Connect HOST and SQL ({first_yyyy} - {last_yyyy}) ***************")
        if first_yyyy == "auto":
            last_month = datetime.today() - relativedelta(months=1)
            yymmdd_host = int(last_month.strftime(r"%Y%m"+"00")) - 19500000
            file_ins.TOTAL_URI.refresh(where=f"伝票日付>={yymmdd_host}")
            file_ins.TEMP_URI1.refresh()
            file_ins.TEMP_URI2.refresh()
            file_ins.ETC_MASTER.refresh()
        else:
            main(
                first_yyyy=first_yyyy,
                last_yyyy =last_yyyy
            )
    except:
        dsp_except()