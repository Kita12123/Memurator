"""
FLASK Main
"""
import os
import pandas as pd
from flask import (
    render_template,
    send_file,
    request,
    send_from_directory,
)
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramFiles.flaskr.setting_ins import SETTING
from ProgramFiles.flaskr.user_ins import USER
from ProgramFiles.query.query_ins import QUERY
from ProgramFiles.query.master_ins import MASTER
from ProgramFiles.totall import TOTALL
from ProgramData import TEMP_CSV
from ProgramFiles.log import CD as LOGCD
from ProgramFiles.db.sql_ins import DB_SQL
from ProgramFiles import db
from ProgramFiles.flaskr import app

#
# Main
#
@app.route("/", methods=["GET"])
def login():
    user_ip = request.remote_addr
    #USER.clear(ip=user_ip)
    user_query = USER.load(ip=user_ip)
    # 順列はそのままだとデータ種類を変更するときに列名がないものを指定してしまう可能性がある
    user_query["順列"] = ""
    user_query["順列タイプ"] = "昇順"
    USER.update(ip=user_ip, query=user_query)
    return render_template(
    # HTML
        "index.html",
        method_type="get",
    # Query data
        user_query=user_query,
    # Display Table of DataFrame
        refresh_date=SETTING.dic["最終更新日時"]
    )
@app.route("/<db_name>", methods=["POST"])
def index(db_name):
    user_ip = request.remote_addr
    # POST
    # Read paramater on request
    user_query = request.form.to_dict()
    if "順列タイプ" not in user_query:
        user_query["順列タイプ"] = "降順"
    USER.update(ip=user_ip, query=user_query)
    # Create Code of SQL for Database on sqlite3
    DB_SQL.db_open()
    df = pd.read_sql(
        sql=QUERY.create_sql_dsp(ip=user_ip,db_name=db_name),
        con=DB_SQL.connection
    )
    DB_SQL.db_close()
    # Message of Count
    # if Count is many, Compression DataFrame for Display
    count=len(df)
    messages = []
    if count >= int(SETTING.dic["最大表示行数"]):
        df_dsp = df.head(int(SETTING.dic["最大表示行数"])).copy()
        count = "{:,} ({})".format(count, int(SETTING.dic["最大表示行数"]))
    else:
        df_dsp = df.copy()
        count = "{:,}".format(count)
    messages.append("合計数量 : {:,}".format(df["数量"].sum()))
    messages.append("合計金額 : ¥{:,}".format(df["金額"].sum()))
    df_dsp.loc[:,("数量","単価","金額")] = df_dsp[["数量","単価","金額"]].applymap("{:,}".format)
    # Totall DataFrame
    df1, df2, df3 = TOTALL.create(df=df)
    return render_template(
    # HTML
        "index.html",
        method_type="post",
    # Query data
        db_name=db_name,
        refresh_date=SETTING.dic["最終更新日時"],
        user_query=USER.load(ip=user_ip),
    # Display Table of DataFrame
        count=count,
        messages=messages,
        headers=df_dsp.columns,
        records=list(list(x) for x in zip(*(df_dsp[x].values.tolist() for x in df_dsp.columns))),
    # Totall Table of DataFrame
        headers_totall1=df1.columns,
        records_totall1=list(list(x) for x in zip(*(df1[x].values.tolist() for x in df1.columns))),
        headers_totall2=df2.columns,
        records_totall2=list(list(x) for x in zip(*(df2[x].values.tolist() for x in df2.columns))),
        headers_totall3=df3.columns,
        records_totall3=list(list(x) for x in zip(*(df3[x].values.tolist() for x in df3.columns))),
    )

@app.route("/search/<column>", methods=["GET", "POST"])
def search(column):
    """抽出条件をマスタより取得"""
    user_ip = request.remote_addr
    # 抽出条件QUERYに反映させる -> "/"へ
    if request.form.get("ok") == "決定":
        user_query = USER.load(ip=user_ip)
        user_query[column] = ",".join(request.form.getlist("key_code"))
        USER.update(ip=user_ip, query=user_query)
        return render_template(
        # HTML
            "index.html",
            method_type="get",
        # Query data
            user_query=USER.load(ip=user_ip),
        # Display Table of DataFrame
            refresh_date=SETTING.dic["最終更新日時"]
        )
    # user_query, master_query作成
    if "順列" in request.form.to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        user_query = request.form.to_dict()
        master_query = {}
    elif request.method == "POST" and request.form.get("ok") == "抽出":
        user_query = USER.load(ip=user_ip)
        master_query = request.form.to_dict()
        user_query[column] = ",".join(request.form.getlist("key_code"))
    USER.update(ip=user_ip, query=user_query)
    selects = MASTER.create_selects(
        column=column,
        value=user_query[column]
    )
    DB_SQL.db_open()
    df = pd.read_sql(
        sql=MASTER.create_sql_dsp(
            column=column,
            form_dic=master_query),
        con=DB_SQL.connection
    )
    DB_SQL.db_close()
    df_dsp = df.head(int(SETTING.dic["最大表示行数"]))
    return render_template(
        "master.html",
        # 抽出input_textをこれで作成しようとしたら難しかった。
        #query_column=MASTER.query_columns,
        master_query=master_query,
        selects=selects,
        refresh_date=SETTING.dic["最終更新日時"],
        headers=["選択"] + list(df_dsp.columns),
        records=list(list(x) for x in zip(*(df_dsp[x].values.tolist() for x in df_dsp.columns)))
    )

@app.route("/<db_name>/download/<flg>", methods=["GET"])
def download(db_name, flg):
    """データをダウンロードする"""
    user_ip = request.remote_addr
    if flg == "table":
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=QUERY.create_sql_download(ip=user_ip,db_name=db_name),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
    else:
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=QUERY.create_sql_dsp(ip=user_ip,db_name=db_name),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
        df1, df2, df3 = TOTALL.create(df=df)
    # To File .csv
    if flg=="totall1":
        df = df1
    elif flg=="totall2":
        df = df2
    elif flg=="totall3":
        df = df3
    df.to_csv(TEMP_CSV, index=False, encoding="cp932", escapechar="|")
    return send_file(
        TEMP_CSV,
        attachment_filename="download.csv"
    )

#
# Setting
#
@app.route("/setting", methods=["GET", "POST"])
def setting():
    """設定画面"""
    log_texts=["ログ内容を表示します"]
    last_month = datetime.today() - relativedelta(months=1)
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            for key in SETTING.dic.keys():
                SETTING.dic[key] = request.form[key]
            SETTING.update()
        elif click == "最新データ取得":
            first_date = request.form.get("first_date")
            db.refresh_all(first_date=first_date.replace("-",""))
        else:
            with open(os.path.join(LOGCD, f"{click}.txt"), mode="r", encoding="utf-8") as f:
                log_texts = f.readlines()
    return render_template(
        "setting.html",
        first_date=last_month.strftime(r"%Y-%m-01"),
        setting_dic=SETTING.dic,
        log_texts=log_texts
    )

@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )