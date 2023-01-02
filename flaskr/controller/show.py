from flask import render_template
from flask import request

from flaskr import app
from flaskr.common import LOGGER
from flaskr.controller.common.user import load_user


@app.route("/show_table", methods=["POST"])
def show_table():
    user = system.load(request.remote_addr)
    user.form.update(**req.form_to_query())
    # Create DataFrame on sqlite3
    df = db.sql.create_df(sql=user.form.to_sql(download=False))
    # Message
    messages = []
    count = len(df)
    if count >= user.max_rows:
        messages.append(f"件数：{count:,} ({user.max_rows})")
    else:
        messages.append(f"件数：{count:,}")
    # Arrange DataFrame
    df1, df2, df3 = arrage_df(df=df)
    columns_sum = [
        c for c in df.columns
        if any([x in c for x in ["数量", "金額"]])
    ]
    for t_c in columns_sum:
        messages.append(f"合計{t_c} : {df[t_c].sum():,}")
    columns_num = [
        c for c in df.columns
        if any([x in c for x in ["数量", "単価", "金額"]])
    ]
    df_dsp = df.head(user.max_rows)
    df_dsp.loc[:, columns_num] = (
        df_dsp[columns_num].applymap("{:,}".format)
    )
    if app.debug:
        LOGGER.debug(
            f"main.show_table\nuser.form.todict(): {user.form.to_dict()}"
        )
    return render_template(
        "show_table.html",
        MyColor=user.mycolor,
        Department=user.department,
        user_form=user.form.to_dict(),
        messages=messages,
        headers=df_dsp.columns,
        records=df_dsp.values.tolist(),
        headers1=df1.columns,
        records1=df1.values.tolist(),
        headers2=df2.columns,
        records2=df2.values.tolist(),
        headers3=df3.columns,
        records3=df3.values.tolist(),
    )