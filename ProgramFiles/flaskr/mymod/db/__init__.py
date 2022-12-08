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
    LOGGER.info(f"ODBC HOST... {ins.table_name_host} ({where_sqlite3})")
    where_host = ins.to_where_host_by(where_sqlite3)
    df = odbc.create_df(sql=ins.select_host_where(where_host))
    # df -> SQLite3
    LOGGER.info(f"Syncing DataBase... {ins.table_name} ({where_sqlite3})")
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
    first_host = int(first_date) - 19500000
    last_host = int(last_date) - 19500000
    refresh(
        host_ins.MUJNRPF_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.UJNRPF_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.UJNRPFW_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.SYUKAPF_FLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.SYUKAPF_FLIBK,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.SYUKAPF_FLIBN,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        host_ins.NSFILEP_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    # refresh(mod.TEHAIPF_KITAURA)
    if contain_master:
        refresh(host_ins.ETCMPF_FLIB)
        refresh(host_ins.NIHONPF_FLIB)
        refresh(host_ins.TOKMPF_FLIB)
        refresh(host_ins.KENPF_FLIB1)
        refresh(host_ins.BUHMPF_FLIB)
        refresh(host_ins.SEIMPF_FLIB)
        refresh(host_ins.RIPPET_FLIB)
        refresh(host_ins.RIPPTR_FLIB)
        refresh(host_ins.PMDBPF_FLIB)
    system.last_refresh_date = datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒")
    LOGGER.info("*************** Ended Connect DataBase ***************")
