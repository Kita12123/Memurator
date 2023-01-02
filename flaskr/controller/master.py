from flask import redirect
from flask import render_template
from flask import request

from flaskr import app
from flaskr.controller.common import read_query_file
from flaskr.model import crud
from flaskr.model import Session


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
