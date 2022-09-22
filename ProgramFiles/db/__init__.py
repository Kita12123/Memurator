"""
Database Package
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramData.setting_ins import SETTING
from ProgramFiles.db import file_ins


def refresh_all():
    """すべてのデータを更新"""
    last_month = datetime.today() - relativedelta(months=1)
    yymmdd_host = int(last_month.strftime(r"%Y%m"+"00")) - 19500000
    file_ins.TOTAL_URI.refresh(where=f"伝票日付>={yymmdd_host}")
    file_ins.TEMP_URI1.refresh()
    file_ins.TEMP_URI2.refresh()
    file_ins.ETC_MASTER.refresh()
    file_ins.SOKCD_MASTER.refresh()
    file_ins.TOKCD_MASTER.refresh()
    #file_ins.KEN_MASTER.refresh()
    #file_ins.BUHIN_MASTER.refresh()
    #file_ins.SEIHIN_MASTER.refresh()
    SETTING.dic["最終更新日時"] = datetime.today().strftime(r"%Y/%m/%d %H:%M:%S")
    SETTING.update()