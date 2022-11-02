"""
FLASK Main
"""
import os
import pandas as pd
from flask import (
    redirect,
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
from ProgramData import cd as LOGCD
from ProgramFiles.db.sql_ins import DB_SQL
from ProgramFiles import db
from ProgramFiles.flaskr import app

#
# Main
#
@app.route("/", methods=["GET"])
def login():
    """初期画面"""
    user_ip = request.remote_addr
    user_query = USER.load(ip=user_ip)
    return render_template(
    # HTML
        "index.html",
        method_type="get",
    # Query data
        user_query=user_query,
    # Setting data
        setting_dic=SETTING.dic
    )

@app.route("/<db_name>", methods=["POST"])
def index(db_name):
    """データ表示"""
    if SETTING.dic["最終更新日時"] == "更新中":
        return redirect("/")
    user_ip = request.remote_addr
    # POST
    # Read paramater on request
    user_query = request.form.to_dict()
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
        setting_dic=SETTING.dic,
        user_query=USER.load(ip=user_ip),
    # Message
        count=count,
        messages=messages,
    # Table
        headers=df_dsp.columns,
        records=df.values.tolist(),
        headers1=df1.columns,
        records1=df1.values.tolist(),
        headers2=df2.columns,
        records2=df2.values.tolist(),
        headers3=df3.columns,
        records3=df3.values.tolist(),
    )

@app.route("/search/<column>", methods=["POST"])
def search(column):
    """抽出条件をマスタより取得"""
    if SETTING.dic["最終更新日時"] == "更新中":
        return redirect("/")
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
            setting_dic=SETTING.dic
        )
    # user_query, master_query作成
    elif "index" in request.form.to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        user_query = request.form.to_dict()
        master_query = {}
    elif request.form.get("ok") == "抽出":
        user_query = USER.load(ip=user_ip)
        master_query = request.form.to_dict()
        user_query[column] = ",".join(request.form.getlist("key_code"))
    USER.update(ip=user_ip, query=user_query)
    selects = MASTER.create_selects(
        column=column,
        value=user_query[column]
    )
    DB_SQL.db_open()
    sql = MASTER.create_sql_dsp(
            column=column,
            form_dic=master_query)
    sql += f" LIMIT {SETTING.dic['最大表示行数']}"
    df = pd.read_sql(
        sql=sql,
        con=DB_SQL.connection
    )
    DB_SQL.db_close()
    return render_template(
        "master.html",
        # 抽出input_textをこれで作成しようとしたら難しかった。
        #query_column=MASTER.query_columns,
        master_query=master_query,
        column=column,
        selects=selects,
        setting_dic=SETTING.dic,
        headers=["選択"] + list(df.columns),
        records=df.values.tolist()
    )

@app.route("/<db_name>/download/<flg>", methods=["GET"])
def download(db_name, flg):
    """データをダウンロードする"""
    if SETTING.dic["最終更新日時"] == "更新中":
        return
    user_ip = request.remote_addr
    if flg == "table":
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=QUERY.create_sql_download(ip=user_ip,db_name=db_name),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
    elif flg == "master":
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=MASTER.create_sql_download(column=db_name),
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
            db.refresh_all(
                first_date=request.form.get("first_date").replace("-",""),
                contain_master=request.form.get("contain_master"))
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