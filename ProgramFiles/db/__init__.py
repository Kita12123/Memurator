"""
Database Package
"""
from datetime import datetime

from ProgramData import DATABASE, SETTING_JSON, USER_JSON
from ProgramFiles.log import LOGGER, dsp_except
from ProgramFiles.db import mod
#
# Initializing
#
host = mod.ConnectOnOdbc(
    connstring="DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
)
sql  = mod.ConnectOnSqlite3(
    database=DATABASE
)
setting = mod.SettingDictionary(
    file_path=SETTING_JSON
)
user = mod.UserDictionary(
    file_path=USER_JSON
)

from ProgramFiles.db import file_ins

def refresh_all(
    first_date: str
    ):
    """すべてのデータを更新"""
    LOGGER.info("*************** Start Connect DataBase ***************")
    try:
        if setting.dic["最終更新日時"] == "更新中":
            return
        setting.dic["最終更新日時"] = "更新中"
        yymmdd_host = int(first_date) - 19500000
        file_ins.MUJNRPF_MOLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.UJNRPF_FLIB1.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.UJNRPFW_FLIB1.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.SYUKAPF_FLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.NSFILEP_MOLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.ETCMPF_FLIB.refresh()
        file_ins.RIPPET_FLIB.refresh()
        file_ins.NIHONPF_FLIB.refresh()
        file_ins.TOKMPF_FLIB.refresh()
        file_ins.RIPPTR_FLIB.refresh()
        file_ins.KENPF_FLIB1.refresh()
        file_ins.BUHMPF_FLIB.refresh()
        file_ins.SEIMPF_FLIB.refresh()
        file_ins.PMDBPF_FLIB.refresh()
        setting.dic["最終更新日時"] = datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒")
    except:
        dsp_except()
        setting.dic["最終更新日時"] = "更新エラー"
    LOGGER.info("*************** Ended Connect DataBase ***************")

def refresh_department(
    first_date: str,
    last_date: str,
    department: str,
    contain_master: bool
    ):
    """すべてのデータを更新"""
    LOGGER.info(f"*************** Start Connect DataBase ({department}) ***************")
    try:
        if setting.dic["最終更新日時"] == "更新中":
            return
        setting.dic["最終更新日時"] = "更新中"
        first_yymmdd_host = int(first_date) - 19500000
        last_yymmdd_host = int(last_date) - 19500000
        if department == "Sales":
            file_ins.MUJNRPF_MOLIB.refresh(
                where=f"伝票日付>={first_yymmdd_host} AND 伝票日付<={last_yymmdd_host}")
            file_ins.UJNRPF_FLIB1.refresh(
                where=f"伝票日付>={first_yymmdd_host} AND 伝票日付<={last_yymmdd_host}")
            file_ins.UJNRPFW_FLIB1.refresh(
                where=f"伝票日付>={first_yymmdd_host} AND 伝票日付<={last_yymmdd_host}")
            file_ins.SYUKAPF_FLIB.refresh(
                where=f"伝票日付>={first_yymmdd_host} AND 伝票日付<={last_yymmdd_host}")
            if contain_master:
                file_ins.ETCMPF_FLIB.refresh()
                file_ins.NIHONPF_FLIB.refresh()
                file_ins.TOKMPF_FLIB.refresh()
                file_ins.KENPF_FLIB1.refresh()
                file_ins.BUHMPF_FLIB.refresh()
                file_ins.SEIMPF_FLIB.refresh()
        elif department == "Plant":
            file_ins.NSFILEP_MOLIB.refresh(
                where=f"伝票日付>={first_yymmdd_host} AND 伝票日付<={last_yymmdd_host}")
            if contain_master:
                file_ins.RIPPET_FLIB.refresh()
                file_ins.RIPPTR_FLIB.refresh()
                file_ins.PMDBPF_FLIB.refresh()
        setting.dic["最終更新日時"] = datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒")
    except:
        dsp_except()
        setting.dic["最終更新日時"] = "更新エラー"
    LOGGER.info(f"*************** Ended Connect DataBase ({department}) ***************")