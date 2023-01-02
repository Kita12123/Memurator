from flask import redirect
from flask import render_template
from flask import request
from pathlib import Path

from flaskr import app
from flaskr.model import Base
from flaskr.model import crud
from flaskr.model import Session

sql_dir = Path(__file__).parent
sql_display_dir = sql_dir / "sql_display"
sql_download_dir = sql_dir / "sql_download"


def read_query_file(filename, /, download=False) -> str:
    if download:
        dir = sql_download_dir
    else:
        dir = sql_display_dir
    with open(dir / filename, mode="r", encoding="utf-8") as f:
        query = f.read()
    return query


@app.route("/master/<db_name>", methods=["GET", "POST"])
def master(db_name):
    query = read_query_file(db_name)
    with Session() as session, session.begin():
        results = session.query(db_cls).all()
    # 抽出条件QUERYに反映させる -> "/"へ
    if request.form.get("ok") == "決定":
        user.form.update(
            **{column: ",".join(request.form.getlist("key_code"))}
        )
        return redirect("/")
    # user_dic, master_query作成
    elif "DB_name" in req.form_to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        user.form.update(**req.form_to_dict())
    elif request.form.get("ok") == "抽出":
        user.form.update(**req.form_to_dict())
        user.form.update(
            **{column: ",".join(request.form.getlist("key_code"))}
        )
    df = db.sql.create_df(sql=user.form.to_sql(download=False))
    # Message
    messages = []
    count = len(df)
    if count >= user.max_rows:
        messages.append(
            "件数：{:,} ({})".format(count, user.max_rows)
        )
    else:
        messages.append("件数：{:,}".format(count))
    df_dsp = df.head(user.max_rows)
    return render_template(
        "master.html",
        user_dic=crud.user_load(request.remote_addr),
        LastRefreshDate=system.last_refresh_date,
        user_form=user.form.to_dict(),
        messages=messages,
        column=column,
        SelectList=user.form.values_for_checkbox(column),
        headers=df_dsp.columns,
        records=df_dsp.values.tolist()
    )
