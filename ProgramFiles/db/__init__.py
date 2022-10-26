"""
Database Package
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramFiles.flaskr.setting_ins import SETTING
from ProgramFiles.db import file_ins
from ProgramFiles.log import LOGGER, dsp_except


def refresh_all(
    first_date = (datetime.today() - relativedelta(months=1)).strftime(r"%Y%m"+"00")
    ):
    """すべてのデータを更新"""
    LOGGER.info("*************** Start Connect DataBase ***************")
    try:
        if SETTING.dic["最終更新日時"] == "更新中":
            return
        SETTING.dic["最終更新日時"] = "更新中"
        SETTING.update()
        yymmdd_host = int(first_date) - 19500000
        file_ins.TOTAL_URI.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.TEMP_URI1.refresh()
        file_ins.TEMP_URI2.refresh()
        file_ins.TOTAL_SYUKA.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.ETC_MASTER.refresh()
        file_ins.SOKCD_MASTER.refresh()
        file_ins.TOKCD_MASTER.refresh()
        #file_ins.KEN_MASTER.refresh()
        file_ins.BUHIN_MASTER.refresh()
        file_ins.SEIHIN_MASTER.refresh()
        SETTING.dic["最終更新日時"] = datetime.today().strftime(r"%Y/%m/%d %H:%M:%S")
        SETTING.update()
    except:
        dsp_except()
        SETTING.dic["最終更新日時"] = "更新エラー"
        SETTING.update()
    LOGGER.info("*************** Ended Connect DataBase ***************")