"""
Database Package
"""
from datetime import datetime

from ProgramData import DATABASE, SYSTEM_JSON, USER_JSON
from ProgramFiles.log import LOGGER, dsp_except
from ProgramFiles.db import mod
#
# Initializing
#
host = mod.ConnectHostOnOdbc(
    connstring="DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
)
sql  = mod.ConnectOnSqlite3(
    database=DATABASE
)
system = mod.SystemDictionary(
    file_path=SYSTEM_JSON
)
user = mod.UserDictionary(
    file_path=USER_JSON
)

from ProgramFiles.db import file_ins

def refresh_all(
    first_date: str
    ):
    """すべてのデータを更新"""
    if system.dic["最終更新日時"] == "更新中":
        return
    LOGGER.info("*************** Start Connect DataBase ***************")
    try:
        system.update(key="最終更新日時", value="更新中")
        yymmdd_host = int(first_date) - 19500000
        file_ins.MUJNRPF_MOLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.UJNRPF_FLIB1.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.UJNRPFW_FLIB1.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.SYUKAPF_FLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.NSFILEP_MOLIB.refresh(where=f"伝票日付>={yymmdd_host}")
        file_ins.TEHAIPF_KITAURA.refresh(if_exists="replace")
        file_ins.ETCMPF_FLIB.refresh()
        file_ins.RIPPET_FLIB.refresh()
        file_ins.NIHONPF_FLIB.refresh()
        file_ins.TOKMPF_FLIB.refresh()
        file_ins.RIPPTR_FLIB.refresh()
        file_ins.KENPF_FLIB1.refresh()
        file_ins.BUHMPF_FLIB.refresh()
        file_ins.SEIMPF_FLIB.refresh()
        file_ins.PMDBPF_FLIB.refresh()
        system.update(
            key="最終更新日時",
            value=datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒"))
    except:
        dsp_except()
        system.dic["最終更新日時"] = "更新エラー"
    LOGGER.info("*************** Ended Connect DataBase ***************")

def refresh_department(
    first_date: str,
    last_date: str,
    department: str,
    contain_master: bool
    ):
    """すべてのデータを更新"""
    if system.dic["最終更新日時"] == "更新中":
        return
    LOGGER.info(f"*************** Start Connect DataBase ({department}) ***************")
    try:
        system.update(key="最終更新日時", value="更新中")
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
            file_ins.TEHAIPF_KITAURA.refresh(if_exists="replace")
            if contain_master:
                file_ins.RIPPET_FLIB.refresh()
                file_ins.RIPPTR_FLIB.refresh()
                file_ins.PMDBPF_FLIB.refresh()
        system.update(
            key="最終更新日時",
            value=datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒"))
    except:
        dsp_except()
        system.dic["最終更新日時"] = "更新エラー"
    LOGGER.info(f"*************** Ended Connect DataBase ({department}) ***************")