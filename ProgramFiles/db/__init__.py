"""
Database Package
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramData import DATABASE, SYSTEM_JSON, USER_JSON
from ProgramFiles.db import mod, file_ins
from ProgramFiles.flaskr import app
from ProgramFiles.flaskr import scheduler

#
# Initializing
#
host = mod.ConnectHostOnOdbc(
    connstring="DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
)
sql = mod.ConnectOnSqlite3(
    database=DATABASE
)
system = mod.SystemDictionary(
    file_path=SYSTEM_JSON
)
user = mod.UserDictionary(
    file_path=USER_JSON
)
# テーブルがなければ作成する
for ins in file_ins.INS_DIC.values():
    sql.update_by_sql(ins.sql_create_table)


#
# Sub Function
#
def refresh(
    ins: mod.HostFileDefine, /, *,
    where_sqlite3: str = "1=1"
) -> None:
    # HOST -> df
    app.logger.debug(f"ODBC HOST... {ins.table_name_host} ({where_sqlite3})")
    where_host = ins.to_where_host_by(where_sqlite3)
    df = host.create_df(sql=ins.select_host_where(where_host))
    # df -> SQLite3
    app.logger.debug(f"Syncing SQL... {ins.table_name} ({where_sqlite3})")
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
    user.save()
    system.save()
    if now_time.strftime(r"%H") in ["08", "10", "12", "14", "16", "18"]:
        today = datetime.today()
        last_month = today - relativedelta(months=1)
        refresh_all(
            first_date=last_month.strftime(r"%Y%m00"),
            last_date=today.strftime(r"%Y%m%d"),
            contain_master=True)


def refresh_all(
    first_date: str,
    last_date: str,
    contain_master: bool
):
    """すべてのデータを更新"""
    if system.dic["最終更新日時"] == "更新中":
        return
    app.logger.info("*************** Start Connect DataBase ***************")
    system.update(key="最終更新日時", value="更新中")
    first_host = int(first_date) - 19500000
    last_host = int(last_date) - 19500000
    refresh(
        file_ins.MUJNRPF_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.UJNRPF_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.UJNRPFW_FLIB1,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.SYUKAPF_FLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.SYUKAPF_FLIBK,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.SYUKAPF_FLIBN,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    refresh(
        file_ins.NSFILEP_MOLIB,
        where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
    )
    # refresh(file_ins.TEHAIPF_KITAURA)
    if contain_master:
        refresh(file_ins.ETCMPF_FLIB)
        refresh(file_ins.NIHONPF_FLIB)
        refresh(file_ins.TOKMPF_FLIB)
        refresh(file_ins.KENPF_FLIB1)
        refresh(file_ins.BUHMPF_FLIB)
        refresh(file_ins.SEIMPF_FLIB)
        refresh(file_ins.RIPPET_FLIB)
        refresh(file_ins.RIPPTR_FLIB)
        refresh(
            file_ins.PMDBPF_FLIB,
            where_sqlite3=f"変更日＊>={first_host} AND 変更日＊<={last_host}"
        )
    system.update(
        key="最終更新日時",
        value=datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒"))
    app.logger.info("*************** Ended Connect DataBase ***************")
