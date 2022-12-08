"""
Database Package
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.db import connect, host_ins
from ProgramFiles.flaskr.mymod.system import system
from ProgramFiles.flaskr import scheduler

#
# Initializing
#
odbc = connect.HostOnOdbc()
sql = connect.DataBaseOnSqlite3()

# テーブルがなければ作成する
for ins in host_ins.INS_DIC.values():
    sql.update_by_sql(ins.sql_create_table)


#
# Sub Function
#
def refresh(
    ins: host_ins.HostFileDefine, /, *,
    where_sqlite3: str = "1=1"
) -> None:
    # HOST -> df
    where_host = ins.to_where_host_by(where_sqlite3)
    df = odbc.create_df(sql=ins.select_host_where(where_host))
    # df -> SQLite3
    if where_sqlite3 == "1=1":
        sql.update_by_sql(ins.sql_deleate_table)
        sql.update_by_sql(ins.sql_create_table)
    else:
        sql.update_by_sql(sql=ins.deleate_sqlite3_where(where_sqlite3))
    sql.update_by_df(
        df=df,
        tablename=ins.table_name,
        if_exists="append",
        index=False)


#
# Main Fucntion
#
@scheduler.task("interval", id="refresh_all", seconds=1*60*60)
def schedule_fuction():
    """定期実行関数"""
    now_time = datetime.now()
    if now_time.strftime(r"%H") in ["08", "10", "12", "14", "16", "18"]:
        last_month = datetime.today() - relativedelta(months=1)
        refresh_all(
            first_date=last_month.strftime(r"%Y%m00"),
            last_date=str(999999 + 19500000),
            contain_master=True)


def refresh_all(
    first_date: str,
    last_date: str,
    contain_master: bool
):
    """すべてのデータを更新"""
    system.last_refresh_date = "更新中"
    LOGGER.info("*************** Start Connect DataBase ***************")
    LOGGER.info(f"データ更新日付: {first_date} ~ {last_date}")
    first_host = int(first_date) - 19500000
    last_host = int(last_date) - 19500000
    LOGGER.info("[1/7] @ーーーーーー Refresh MUJNRPF.MOLIB...")
    refresh(
        host_ins.MUJNRPF_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[2/7] @@ーーーーー Refresh UJNRPF.FLIB1...")
    refresh(
        host_ins.UJNRPF_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[3/7] @@@ーーーー Refresh UJNRPFW.FLIB1...")
    refresh(
        host_ins.UJNRPFW_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[4/7] @@@@ーーー Refresh SYUKAPF.FLIB...")
    refresh(
        host_ins.SYUKAPF_FLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[5/7] @@@@@ーー Refresh SYUKAPF.FLIBK...")
    refresh(
        host_ins.SYUKAPF_FLIBK,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[6/7] @@@@@@ー Refresh SYUKAPF.FLIBN...")
    refresh(
        host_ins.SYUKAPF_FLIBN,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    LOGGER.info("[7/7] @@@@@@@ Refresh NSFILEP.MOLIB...")
    refresh(
        host_ins.NSFILEP_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    # refresh(mod.TEHAIPF_KITAURA)
    if contain_master:
        LOGGER.info("マスタ更新")
        LOGGER.info("[1/9] @ーーーーーーーー Refresh ETCMPF.FLIB...")
        refresh(host_ins.ETCMPF_FLIB)
        LOGGER.info("[2/9] @@ーーーーーーー Refresh NIHONPF.FLIB...")
        refresh(host_ins.NIHONPF_FLIB)
        LOGGER.info("[3/9] @@@ーーーーーー Refresh TOKMPF.FLIB...")
        refresh(host_ins.TOKMPF_FLIB)
        LOGGER.info("[4/9] @@@@ーーーーー Refresh KENPF.FLIB1...")
        refresh(host_ins.KENPF_FLIB1)
        LOGGER.info("[5/9] @@@@@ーーーー Refresh BUHMPF.FLIB...")
        refresh(host_ins.BUHMPF_FLIB)
        LOGGER.info("[6/9] @@@@@@ーーー Refresh SEIMPF.FLIB...")
        refresh(host_ins.SEIMPF_FLIB)
        LOGGER.info("[7/9] @@@@@@@ーー Refresh RIPPET.FLIB...")
        refresh(host_ins.RIPPET_FLIB)
        LOGGER.info("[8/9] @@@@@@@@ー Refresh RIPPTR.FLIB...")
        refresh(host_ins.RIPPTR_FLIB)
        LOGGER.info("[9/9] @@@@@@@@@ Refresh PMDBPF.FLIB...")
        refresh(host_ins.PMDBPF_FLIB)
    system.last_refresh_date = datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒")
    LOGGER.info(f"データ更新日付: {first_date} ~ {last_date}")
    LOGGER.info("*************** Ended Connect DataBase ***************")
