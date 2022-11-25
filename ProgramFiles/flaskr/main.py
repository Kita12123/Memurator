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
from ProgramFiles.flaskr import app, mod
from ProgramFiles import db, log
from ProgramFiles import query as qry

#
# Main
#
@app.route("/", methods=["GET", "POST"])
def index():
    """部署割り当て"""
    user_ip = request.remote_addr
    if request.method == "POST":
        # 更新
        db.user.update(key=user_ip, dic=request.form.to_dict())
    elif "Department" not in db.user.load(key=user_ip):
        # 作成
        return render_template("index.html")
    elif "MyColor" not in db.user.load(key=user_ip):
        db.user.update(key=user_ip, dic={"MyColor":"default"})
        return redirect("/form")
    else:
        # フォーム画面へ
        return redirect("/form")

@app.route("/form", methods=["GET"])
def form():
    """フォーム画面"""
    return render_template(
        "form.html",
        user_dic=db.user.load(key=request.remote_addr),
        system_dic=db.system.dic
    )

@app.route("/show_table", methods=["GET", "POST"])
def show_table():
    """データ表示"""
    if request.method == "GET":
        redirect("/form")
    user_ip = request.remote_addr
    db.user.update(key=user_ip, dic=request.form.to_dict())
    user_dic = db.user.load(key=user_ip)
    # Create DataFrame on sqlite3
    db.sql.open()
    df = pd.read_sql(
        sql=qry.CreateSqlCode(query=user_dic, download=False),
        con=db.sql.connection
    )
    db.sql.close()
    # Message
    messages = []
    count=len(df)
    if count >= db.system.max_display_lines:
        messages.append("件数：{:,} ({})".format(count, db.system.max_display_lines))
    else:
        messages.append("件数：{:,}".format(count))
    # Arrange DataFrame
    messages.append("合計数量 : {:,}".format(df["数量"].sum()))
    messages.append("合計金額 : ¥{:,}".format(df["金額"].sum()))
    df1, df2, df3 = mod.arrage_df(df=df)
    df_dsp = df.head(db.system.max_display_lines)
    df_dsp.loc[:,("数量","単価","金額")] = df_dsp[["数量","単価","金額"]].applymap("{:,}".format)
    return render_template(
        "show_table.html",
        user_dic=user_dic,
        system_dic=db.system.dic,
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
    user_ip = request.remote_addr
    # 抽出条件QUERYに反映させる -> "/"へ
    if request.form.get("ok") == "決定":
        db.user.update(
            key=user_ip,
            dic={column : ",".join(request.form.getlist("key_code"))})
        return redirect("/form")
    # user_dic, master_query作成
    elif "データ名" in request.form.to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        db.user.update(key=user_ip, dic=request.form.to_dict())
        master_query = {}
    elif request.form.get("ok") == "抽出":
        master_query = request.form.to_dict()
        del master_query["ok"]
        if "key_code" in master_query:
            del master_query["key_code"]
        db.user.update(
            key=user_ip,
            dic={column : ",".join(request.form.getlist("key_code"))})
    user_dic = db.user.load(key=user_ip)
    db.sql.open()
    df = pd.read_sql(
        sql=qry.ReadSqlFile(
                db_name=user_dic["データ名"],
                download=False
            ).format(qry.CreateWhereCodeMaster(master_query)),
        con=db.sql.connection
    )
    db.sql.close()
    # Message
    messages = []
    count=len(df)
    if count >= db.system.max_display_lines:
        messages.append("件数：{:,} ({})".format(count, db.system.max_display_lines))
    else:
        messages.append("件数：{:,}".format(count))
    df_dsp = df.head(db.system.max_display_lines)
    return render_template(
        "master.html",
    # QUERY
        user_dic=user_dic,
        system_dic=db.system.dic,
        messages=messages,
        master_query=master_query,
        column=column,
        SelectList=qry.SelectList(column=column, value=user_dic[column]),
        headers=df_dsp.columns,
        records=df_dsp.values.tolist()
    )

@app.route("/download/<flg>", methods=["GET"])
def download(flg):
    """データをダウンロードする"""
    user_ip = request.remote_addr
    user_dic = db.user.load(key=user_ip)
    if flg == "table":
        db.sql.open()
        df = pd.read_sql(
            sql=qry.CreateSqlCode(query=user_dic, download=True),
            con=db.sql.connection
        )
        db.sql.close()
    elif flg == "master":
        df = pd.read_sql(
            sql=( qry.ReadSqlFile(
                db_name=user_dic["データ名"],
                download=False
                ).format("WHERE 1=1")
                + f" LIMIT {db.system.max_display_lines}"
            ),
            con=db.sql.connection
        )
        db.sql.close()
    else:
        db.sql.open()
        df = pd.read_sql(
            sql=qry.CreateSqlCode(query=user_dic, download=True),
            con=db.sql.connection
        )
        db.sql.close()
        df1, df2, df3 = mod.arrage_df(df=df)
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
        download_name="download.csv"
    )

#
# Setting
#
@app.route("/setting", methods=["GET", "POST"])
def setting():
    """設定画面"""
    user_ip = request.remote_addr
    user_dic = db.user.load(key=user_ip)
    with open(os.path.join(SYSTEMDIR, f"debug.txt"), mode="r", encoding="utf-8") as f:
        log_texts = f.readlines()[-1:]
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            for k, v in request.form.to_dict().items():
                if k in db.system.dic:
                    db.system.update(key=k, value=v)
                if k in user_dic:
                    user_dic[k] = v
            db.system.save()
            db.user.update(key=user_ip, dic=user_dic)
        elif click == "最新データ取得":
            db.user.save()
            db.refresh_department(
                first_date=request.form.get("first_date").replace("-",""),
                last_date =request.form.get("last_date").replace("-",""),
                department=user_dic["Department"],
                contain_master=request.form.get("contain_master"))
        else:
            with open(os.path.join(SYSTEMDIR, f"{click}.txt"), mode="r", encoding="utf-8") as f:
                log_texts = f.readlines()
    return render_template(
        "setting.html",
    # QUERY
        user_dic=user_dic,
        system_dic=db.system.dic,
        first_date=(datetime.today() - relativedelta(months=1)).strftime(r"%Y-%m-01"),
        last_date =datetime.now().strftime((r"%Y-%m-%d")),
        log_texts=log_texts
    )

@app.route("/admin", methods=["GET","POST"])
def admin():
    """管理者画面"""
    sql_code = ""
    values = []
    if request.method == "POST":
        sql_code = request.form.get("sql_code")
        db.sql.open()
        try:
            db.sql.execute(sql=sql_code)
            values = db.sql.cursor.fetchall()
            db.sql.commit()
            db.sql.close()
        except:
            values = log.traceback.format_exc()
            db.sql.close()
    return render_template(
        "admin.html",
        sql_code=sql_code,
        values=values
    )

@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )