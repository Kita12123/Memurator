"""
Database Package
"""
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramData import M_SETTING_PATH
from ProgramFiles.db import func, file_ins

#
# Sub Function
#
def Rewrite_Refresh_Time(memo=""):
    """最終更新日時を現在日時に上書きする"""
    with open(M_SETTING_PATH, mode="r") as f:
        tmp_dic = json.load(f)
        tmp_dic["最終更新日時"] = datetime.today().strftime(r"%Y/%m/%d %H:%M:%S") + memo
    with open(M_SETTING_PATH, mode="w") as f:
        json.dump(tmp_dic, f, indent=1)

#
# Main
#
def create_uriage_df(
    sql_where_sqlite3: str,
    sort_column: str,
    sort_type: str
    ) -> tuple[func.pd.DataFrame, str]:
    # データ取得
    sql=func.craft_sql(
        sql_where_sqlite3=sql_where_sqlite3,
        sort_column=sort_column,
        sort_type=sort_type
    )
    df = func.create_df_sqlite3(
        sql=sql
    )
    return df, sql

def refresh_auto():
    last_month = datetime.today() - relativedelta(months=1)
    yymmdd_host = int(last_month.strftime(r"%Y%m"+"00")) - 19500000
    file_ins.TOTAL_URI.refresh(sql=f"伝票日付>={yymmdd_host}")
    file_ins.TEMP_URI1.refresh()
    file_ins.TEMP_URI2.refresh()
    file_ins.ETC_MASTER.refresh()
    Rewrite_Refresh_Time()