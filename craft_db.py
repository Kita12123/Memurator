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
import json
from dateutil.relativedelta import relativedelta
import sys

from ProgramData import M_SETTING_PATH
from ProgramFiles.db import file_ins
from ProgramFiles.log import LOGGER, dsp_except

#
# Sub Function
#
def Rewrite_Refresh_Time(memo=""):
    with open(M_SETTING_PATH, mode="r", encoding="cp932") as f:
        tmp_dic = json.load(f)
        tmp_dic["REFRESH_DATE"] = datetime.today().strftime(r"%Y/%m/%d %H:%M:%S") + memo
    with open(M_SETTING_PATH, mode="w", encoding="cp932") as f:
        json.dump(tmp_dic, f, indent=1)

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
            file_ins.TOTAL_URI.refresh(sql=f"伝票日付>={yymmdd_host}")
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
    Rewrite_Refresh_Time()