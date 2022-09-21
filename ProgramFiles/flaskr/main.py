"""
FLASK Main
"""
import os
from flask import (
    render_template,
    url_for,
    send_file,
    request,
    send_from_directory
)
from datetime import datetime, timedelta
import json

from ProgramData import M_SETTING_PATH
from ProgramFiles.flaskr import app
from ProgramFiles.log import LOGGER, CD as LOGCD
from ProgramFiles import db

#
# Sub Function
#
def create_sql_dennpyou_date(fd: str, ld: str) -> str:
    """Adjust Date from YYYY-MM-DD to YYYYMMDD"""
    if fd == "":
        first = ""
    else:
        fd_ = int(fd.replace("-","")) - 19500000
        first = f" 伝票日付>={fd_} AND\n"
    if ld == "":
        last = ""
    else:
        ld_ = int(ld.replace("-","")) - 19500000
        last = f" 伝票日付<={ld_} AND\n"
    return first + last

def create_sql_seihin_buhin_cd(cd: str) -> str:
    """製品部品コードのSQLコードを作成"""
    def func(c: str):
        c = c.replace(" ", "")
        if c.isdigit():
            if len(c) == 5:
                return f" OR ( 製品部品コード>={c}00 AND 製品部品コード<={c}99 ) "
            return f" OR 製品部品コード={c} "
        else:
            return f" OR 製品部品カナ LIKE'%{c}%' "
    if cd == "":
        return ""
    elif "," in cd:
        # ','区切りにORで結合した、SQLコードを作成する
        sql = "".join([func(code) for code in cd.split(",")])[3:]
        return f" ({sql}) AND\n"
    else:
        return func(cd)[3:] + " AND\n"

def create_sql_seihin_buhin_flg(flg: str) -> str:
    """製品のみ部品のみのSQLコードを作成"""
    if   flg == "seihin":
        return " 製品部品コード<= 9999999 AND \n"
    elif flg == "buhin":
        return " 製品部品コード>=10000000 AND \n"
    else:
        return ""

def create_sql_tokuisaki_cd(cd: str) -> str:
    """得意先コードのSQLコードを作成"""
    def func(c: str):
        c = c.replace(" ", "")
        if c.isdigit():
            if len(c) <= 4:
                # 3ｹﾀでも対応する
                z = '0'*(4 - len(c))
                return f" OR ( 得意先コード>={z}{c}00 AND 得意先コード<={z}{c}99 ) "
            return f" OR 得意先コード={c} "
        else:
            return f" OR 得意先カナ LIKE'%{c}%' "
    if cd == "":
        return ""
    elif "," in cd:
        sql = "".join([ func(code) for code in cd.split(",")])[3:]
        return f" ({sql}) AND\n"
    else:
        return func(cd)[3:] + " AND \n"

def create_sql_soukasaki_cd(cd: str) -> str:
    """送荷先コードのSQLコード作成"""
    def func(c: str):
        if c.isdigit():
            return f" OR 送荷先コード={c} "
        else:
            return f" OR 送荷先カナ LIKE'%{c}%' "
    if cd == "":
        return ""
    elif "," in cd:
        sql = "".join([ func(code) for code in cd.split(",")])[3:]
        return f" ({sql}) AND\n"
    else:
        return func(cd)[3:] + " AND \n"

def create_sql_zatu_cd(cd: str) -> str:
    """雑コードのSQLコード作成"""
    def func(c: str):
        if c.isdigit():
            return f" OR 雑コード={c} "
        else:
            return ""
    if cd == "":
        return ""
    elif "," in cd:
        sql = "".join([ func(code) for code in cd.split(",")])[3:]
        return f" ({sql}) AND\n"
    else:
        return func(cd)[3:] + " AND \n"

#
# Main
#
@app.route("/", methods=["GET","POST"])
def index():
    LOGGER.debug("リクエスト取得")
    with open(M_SETTING_PATH, mode="r", encoding="cp932") as f:
        setting_dic = json.load(f)
    max_dsp_row = int(setting_dic["最大表示行数"])
    refresh_date = setting_dic["最終更新日時"]
    if request.method=="GET":
        return render_template(
        # HTML
            "index.html",
            method_type="get",
        # Query data
            first_yyyy_mm_dd=( datetime.today() - timedelta(days=1) ).strftime(r"%Y-%m-%d"),
            last_yyyy_mm_dd=datetime.today().strftime(r"%Y-%m-%d"),
            sort_type="昇順",
        # Display Table of DataFrame
            refresh_date=refresh_date,
            headers=["抽出条件を入力してください。"]
        )
    # Read paramater on request
    first_yyyy_mm_dd = request.form["first_yyyy_mm_dd"]
    last_yyyy_mm_dd = request.form["last_yyyy_mm_dd"]
    seihin_buhin_cd = request.form["seihin_buhin_cd"]
    seihin_buhin_flg = request.form["seihin_buhin_flg"]
    tokuisaki_cd = request.form["tokuisaki_cd"]
    zatu_cd = request.form["zatu_cd"]
    soukasaki_cd = request.form["soukasaki_cd"]
    sort_column = request.form["sort_column"]
    sort_type = request.form.get("sort_type","降順")
    # Create Code of SQL for Database on sqlite3
    # HOSTとsqlite3で送荷先コードのタイプが違うため、それぞれのSQLコードが必要
    sql_where_sqlite3 = (
        "/* ユーザー抽出条件 */\n"
    +   create_sql_dennpyou_date(fd=first_yyyy_mm_dd, ld=last_yyyy_mm_dd)
    +   create_sql_tokuisaki_cd(cd=tokuisaki_cd)
    +   create_sql_zatu_cd(cd=zatu_cd)
    +   create_sql_soukasaki_cd(soukasaki_cd)
    +   create_sql_seihin_buhin_cd(cd=seihin_buhin_cd)
    +   create_sql_seihin_buhin_flg(flg=seihin_buhin_flg)
    )[:-5] + "\n/* ユーザー抽出条件 */"
    # Create DataFrame
    LOGGER.debug("SQL接続")
    df, sql_sqlite3 = db.create_uriage_df(
        sql_where_sqlite3=sql_where_sqlite3,
        sort_column=sort_column,
        sort_type=sort_type
    )
    # Message of Count
    # if Count is many, Compression DataFrame for Display
    count=len(df)
    messages = []
    if count >= max_dsp_row:
        df_dsp = df.head(max_dsp_row)
        messages.append("件数 : {:,} ({})".format(count, max_dsp_row))
    else:
        df_dsp = df
        messages.append("件数 : {:,}".format(count))
    messages.append("合計数量 : {:,}".format(df["数量"].sum()))
    messages.append("合計金額 : ¥{:,}".format(df["金額"].sum()))
    LOGGER.debug("POST出力")
    return render_template(
    # HTML
        "index.html",
        method_type="post",
    # Query data
        sql_sqlite3=sql_sqlite3,
        first_yyyy_mm_dd=first_yyyy_mm_dd,
        last_yyyy_mm_dd=last_yyyy_mm_dd,
        seihin_buhin_cd=seihin_buhin_cd,
        seihin_buhin_flg=seihin_buhin_flg,
        tokuisaki_cd=tokuisaki_cd,
        zatu_cd=zatu_cd,
        soukasaki_cd=soukasaki_cd,
        sort_column=sort_column,
        sort_type=sort_type,
    # for download
        sql_where_sqlite3=sql_where_sqlite3,
    # Totalling User DataFrame
        count=count,
        messages=messages,
    # Display Table of DataFrame
        refresh_date=refresh_date,
        headers=df_dsp.columns,
        records=list(list(x) for x in zip(*(df_dsp[x].values.tolist() for x in df_dsp.columns))),
    )

@app.route("/download", methods=["POST"])
def download():
    """データをダウンロードする"""
    sql_where_sqlite3 = request.form["sql_where_sqlite3"]
    sort_column = request.form["sort_column"]
    sort_type = request.form["sort_type"]
    file = os.path.join(app.root_path, "download.csv")
    df, sql_sqlite3 = db.create_uriage_df(
        sql_where_sqlite3=sql_where_sqlite3,
        sort_column=sort_column,
        sort_type=sort_type
    )
    df.to_csv(file, index=False, encoding="cp932", escapechar="|")
    return send_file(
        file,
        attachment_filename="data.csv"
    )

#
# Setting
#
@app.route("/setting", methods=["GET", "POST"])
def setting():
    """設定画面"""
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            with open(M_SETTING_PATH, mode="r") as f:
                setting_dic = json.load(f)
            for key in setting_dic.keys():
                setting_dic[key] = request.form[key]
            with open(M_SETTING_PATH, mode="w") as f:
                json.dump(setting_dic, f, indent=1)
        elif click == "最新データ取得":
            db.refresh_auto()
    with open(M_SETTING_PATH, mode="r") as f:
        setting_dic = json.load(f)
    with open(os.path.join(LOGCD, "debug.txt"), mode="r", encoding="utf-8") as f:
        log_texts = f.readlines()
    print(log_texts)
    return render_template(
        "setting.html",
        now=datetime.today().strftime(r"%Y/%m/%d %H:%M:%S"),
        setting_dic=setting_dic,
        refresh_date=setting_dic["最終更新日時"],
        log_texts=log_texts
    )

@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )