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


from ProgramData import TEMP_CSV, SYSTEMDIR
from ProgramFiles.flaskr.user_ins import USER
from ProgramFiles.flaskr.setting_ins import SETTING
from ProgramFiles.db.sql_ins import DB_SQL
from ProgramFiles.flaskr import ArrangeDataFrame as age
from ProgramFiles import query as qry
from ProgramFiles import db
from ProgramFiles.flaskr import app

#
# Main
#
@app.route("/", methods=["GET", "POST"])
def index():
    """部署割り当て"""
    user_ip = request.remote_addr
    user_query = USER.load(ip=user_ip)
    if request.method == "POST":
        user_query["Department"] = request.form.get("Department")
        USER.update(ip=user_ip, query=user_query)
    if "Department" not in user_query:
        return render_template("index.html")
    else:
        return redirect("/query")

@app.route("/query", methods=["GET"])
def query():
    """フォーム画面"""
    return render_template(
        "query.html",
    # QUERY
        user_query=USER.load(ip=request.remote_addr),
        setting_dic=SETTING.dic
    )

@app.route("/show_table", methods=["POST"])
def show_table():
    """データ表示"""
    if SETTING.dic["最終更新日時"] == "更新中":
        return redirect("/")
    user_ip = request.remote_addr
    user_query = USER.load(ip=user_ip)
    user_query.update(request.form.to_dict())
    USER.update(ip=user_ip, query=user_query)
    # Create DataFrame on sqlite3
    DB_SQL.db_open()
    df = pd.read_sql(
        sql=qry.CreateSqlCode(query=user_query, download=False),
        con=DB_SQL.connection
    )
    DB_SQL.db_close()
    # Message
    messages = []
    count=len(df)
    if count >= int(SETTING.dic["最大表示行数"]):
        messages.append("件数：{:,} ({})".format(count, int(SETTING.dic["最大表示行数"])))
    else:
        messages.append("件数：{:,}".format(count))
    # Arrange DataFrame
    messages.append("合計数量 : {:,}".format(df["数量"].sum()))
    messages.append("合計金額 : ¥{:,}".format(df["金額"].sum()))
    df1, df2, df3 = age.Totall(df=df)
    df_dsp = df.head(int(SETTING.dic["最大表示行数"]))
    df_dsp.loc[:,("数量","単価","金額")] = df_dsp[["数量","単価","金額"]].applymap("{:,}".format)
    return render_template(
        "show_table.html",
    # QUERY
        user_query=user_query,
        setting_dic=SETTING.dic,
    # Message
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
    user_query = USER.load(ip=user_ip)
    # 抽出条件QUERYに反映させる -> "/"へ
    if request.form.get("ok") == "決定":
        user_query[column] = ",".join(request.form.getlist("key_code"))
        USER.update(ip=user_ip, query=user_query)
        return redirect("/query")
    # user_query, master_query作成
    elif "データ名" in request.form.to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        user_query.update(request.form.to_dict())
        master_query = {}
    elif request.form.get("ok") == "抽出":
        user_query = USER.load(ip=user_ip)
        master_query = request.form.to_dict()
        user_query[column] = ",".join(request.form.getlist("key_code"))
    USER.update(ip=user_ip, query=user_query)
    DB_SQL.db_open()
    df = pd.read_sql(
        sql=( qry.ReadSqlFile(
            db_name=user_query["データ名"],
            download=False).format(
                qry.CreateWhereCodeMaster(master_query))
            + f" LIMIT {SETTING.dic['最大表示行数']}"
        ),
        con=DB_SQL.connection
    )
    DB_SQL.db_close()
    return render_template(
        "master.html",
    # QUERY
        user_query=user_query,
        setting_dic=SETTING.dic,
        master_query=master_query,
        column=column,
        SelectList=qry.SelectList(column=column, value=user_query[column]),
        headers=["選択"] + list(df.columns),
        records=df.values.tolist()
    )

@app.route("/download/<flg>", methods=["GET"])
def download(flg):
    """データをダウンロードする"""
    if SETTING.dic["最終更新日時"] == "更新中":
        return
    user_ip = request.remote_addr
    user_query = USER.load(ip=user_ip)
    if flg == "table":
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=qry.CreateSqlCode(query=user_query, download=True),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
    elif flg == "master":
        df = pd.read_sql(
            sql=( qry.ReadSqlFile(
                db_name=user_query["データ名"],
                download=False
                ).format("WHERE 1=1")
                + f" LIMIT {SETTING.dic['最大表示行数']}"
            ),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
    else:
        DB_SQL.db_open()
        df = pd.read_sql(
            sql=qry.CreateSqlCode(query=user_query, download=True),
            con=DB_SQL.connection
        )
        DB_SQL.db_close()
        df1, df2, df3 = age.Totall(df=df)
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
    user_ip = request.remote_addr
    user_query = USER.load(ip=user_ip)
    log_texts=["ログ内容を表示します"]
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            for k, v in request.form.to_dict().items():
                if k in SETTING.dic:
                    SETTING.dic[k] = v
                if k in user_query:
                    user_query[k] = v
            SETTING.update()
            USER.update(ip=user_ip, query=user_query)
        elif click == "最新データ取得":
            db.refresh_all(
                first_date=request.form.get("first_date").replace("-",""),
                contain_master=request.form.get("contain_master"))
        else:
            with open(os.path.join(SYSTEMDIR, f"{click}.txt"), mode="r", encoding="utf-8") as f:
                log_texts = f.readlines()
    return render_template(
        "setting.html",
    # QUERY
        user_query=user_query,
        setting_dic=SETTING.dic,
        first_date=(datetime.today() - relativedelta(months=1)).strftime(r"%Y-%m-01"),
        log_texts=log_texts
    )

@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )